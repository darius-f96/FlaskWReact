from crypt import methods
from unicodedata import name
from classes.Employee import Employees
from classes.Organization import Organizations, Organization
from flask import Flask, jsonify, request
import requests, json, re
#graphql libraries
from gql import Client, gql
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
#rdf
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

app = Flask(__name__)

prefix = URIRef("http://grafexamen#")

app.config['server1_host'] = "localhost"
app.config['server1_port'] = '4000'

app.config['server2_host'] = "localhost"
app.config['server2_port'] = '3000'

app.config['server3_host'] = "192.168.0.186"
app.config['server3_port'] = '8080'
app.config['server3_burl'] = 'rdf4j-server/repositories/grafexamen'

@app.route('/hello/<name>')
def hello_world(name):
   return 'Hello, %s, senior python dev' % name

@app.route('/getdata1', methods = ["GET"])
def get_data1():
   resp_db = requests.get('http://{}:{}/db/'.format(app.config['server1_host'], app.config['server1_port']))
   return resp_db.content

@app.route('/addOrg', methods = ["POST"])
def addOrg():
   resp_db = requests.get('http://{}:{}/organizations/'.format(app.config['server1_host'], app.config['server1_port']))
   json_obj = json.loads(resp_db.content)
   org_array = Organizations()
   for org_dict in json_obj:
      org_array.addOrg(org_dict)
   
   if request.method == "POST":
      json_obj = json.loads(request.data)
      if org_array.exists(json_obj):
         return jsonify("Organization already exists"), 300
      else:
         #push it to db
         org_array.addOrg(json_obj)
         resp_db = requests.post('http://{}:{}/organizations'.format(app.config['server1_host'], app.config['server1_port']),
                                 org_array.getAll()[-1].toJson())
         return resp_db.json()

@app.route('/addEmp', methods = ["POST"])
def addEmp():
   resp_db = requests.get('http://{}:{}/organizations/'.format(app.config['server1_host'], app.config['server1_port']))
   json_obj = json.loads(resp_db.content)
   org_array = Organizations()
   for org_dict in json_obj:
      org_array.addOrg(org_dict)
   
   #get employee data
   resp_db = requests.get('http://{}:{}/employees/'.format(app.config['server1_host'], app.config['server1_port']))
   json_obj = json.loads(resp_db.content)
   emp_array = Employees()
   for emp_dict in json_obj:
      emp_array.addEmp(emp_dict)

   json_obj = json.loads(request.data)
   if emp_array.exists(json_obj):
      return jsonify("Employee already exists, try using a different name"), 300
   orgdbId = org_array.getIdByName(json_obj)
   if  orgdbId == 0:
      return jsonify("Organization used does not exists, try using a different one or create the organization"), 300
   else:
      #push it to db
      json_obj['organizationId'] = orgdbId
      emp_array.addEmp(json_obj)
      resp_db = requests.post('http://{}:{}/employees'.format(app.config['server1_host'], app.config['server1_port']),
                              emp_array.getAll()[-1].toJson())
      return resp_db.json()

@app.route('/postToGraphql', methods = ["POST"])
def postToGraphql():

   json_obj = json.loads(request.data)
   employeeArray = []

   for initialOrg in json_obj:
      for initialEmployee in initialOrg['employees']:
         initialEmployee['organization_id'] = initialEmployee['organizationId']
         del initialEmployee['organizationId']
         employeeArray.append(initialEmployee)
      del initialOrg['employees']

   transport = RequestsHTTPTransport(url='http://{}:{}/'.format(app.config['server2_host'], app.config['server2_port']), verify=True, retries=3,)

   client = Client(transport=transport, fetch_schema_from_transport=True)
   mutation = gql(
      """
         mutation createManyOrganizationData($dat: [OrganizationInput]) { 
            createManyOrganization(data: $dat)
               {
                  id
                  name
                  cui  
               }
               }
      """
   )
   params = {
      "dat" : json_obj
   }
   result = client.execute(mutation, variable_values=params)
   
   for resultedOrg in result['createManyOrganization']:
      for initialOrg in json_obj:
         for initialEmp in employeeArray:
            if resultedOrg['name'] == initialOrg['name'] and initialEmp['organization_id'] == initialOrg['id']:
               initialEmp['organization_id'] = resultedOrg['id']

   mutation = gql(
         """
            mutation createManyEmployeeData($dat: [EmployeeInput]) { 
               createManyEmployee(data: $dat)
                  {
                     id
                     firstname
                     lastname
                     age
                     organization_id 
                  }
                  }
         """
      )
   params = {
         "dat" : employeeArray
      }
   
   result = client.execute(mutation, variable_values=params)
   return {
      "code": 200,
      "message": "Data was added successfuly"
   }

@app.route('/getOrgWEmployees', methods = ["GET"])
def getOrgWEmployeeLink():
   resp_db = requests.get('http://{}:{}/organizations?_embed=employees'.format(app.config['server1_host'], app.config['server1_port']))
   return resp_db.content

@app.route('/getOrgWEmployeesS2')
def get_data2():

   transport = RequestsHTTPTransport(url='http://{}:{}/'.format(app.config['server2_host'], app.config['server2_port']), verify=True, retries=3,)

   client = Client(transport=transport, fetch_schema_from_transport=True)

   query = gql(

   """
      {
         allOrganizations {
               id
               name
               cui
               Employees {
                  id
                  firstname
                  lastname
                  organization_id
                  age
               }
      
         }
      }

   """

   )

   result = client.execute(query)
   #result_changed = {}
   #result_changed['Organizations'] = 
   return jsonify(result['allOrganizations'])

@app.route('/getOrgWEmployeesS3')
def get_rdf4j_statements():

   gr = Graph()
   payload = "construct {?s ?p ?o} where {?s ?p ?o}"
   headers = {
   'Content-Type': 'application/sparql-query'
   }
   organizationArray = Organizations()
   employeeArray = Employees()
   response = requests.post('http://{}:{}/{}'.format(app.config['server3_host'], app.config['server3_port'], app.config['server3_burl']), headers=headers, data=payload)

   gr.parse(response.content)

   for sub in gr.subjects():
      ent = {}
      s = re.sub(prefix, '', sub)
      ent['id'] = s
      print ('subject passing by : ' + s)
      for pred in gr.predicates(sub):
         p = re.sub(prefix, '', pred)
         for value in gr.objects(sub, pred):
            v = re.sub(prefix, '', value)
            if p == 'Name':
               ent['name'] = v
            elif p == 'CUI':
               ent['cui'] = v
            elif p == 'hasFirstName':
               ent['firstname'] = v
            elif p == 'hasLastName':
               ent['lastname'] = v
            elif p == 'hasAge':
               ent['age'] = v
            elif p =='employeeOf':
               ent['organizationId'] = v
            else:
               continue
      if 'cui' in ent:
         organizationArray.addOrg(ent)
      else:
         employeeArray.addEmp(ent)

   response = organizationArray.getAllJson()
   for o in response:
      for e in employeeArray.getAllJson():
         if 'organizationId' in e and e['organizationId'] == o['id']:
            if not 'Employees' in o:
               o['Employees'] = []
            o['Employees'].append(e)

   return jsonify(response)

@app.route('/postToRdf4j', methods=["POST"])
def add_rdf4j_statements():
   json_obj = json.loads(request.data)
   employeeArray = Employees()
   organizationArray = Organizations()

   for initialOrg in json_obj:
      for initialEmployee in initialOrg['Employees']:
         initialEmployee['organizationId'] = initialEmployee['organization_id']
         del initialEmployee['organization_id']
         employeeArray.addEmp(initialEmployee)
      del initialOrg['Employees']
      organizationArray.addOrg(initialOrg)

   gr = Graph()

   for obj in employeeArray.getAll():
      obj.addToGraph(gr)
   
   for obj in organizationArray.getAll():
      obj.addToGraph(gr)

   payload = gr.serialize(format='turtle')
   headers = {
   'Content-Type': 'application/x-turtle;charset=UTF-8'
   }

   response = requests.put('http://{}:{}/{}/statements'.format(app.config['server3_host'], app.config['server3_port'], app.config['server3_burl']), headers=headers, data=payload)

   if response.content == "":
      return {
      "code": 200,
      "message": "Data was added successfuly"
   }
   else:
      return response.content

@app.route('/addCryptoData', methods=["POST"])
def addCryptoData():
   crypto = json.loads(request.data)
   print (crypto)
   gr = Graph()

   gr.add((prefix+crypto['symbol'], prefix+"hasPrice", prefix+ Literal("$"+crypto['price'], datatype=XSD.decimal)))
   gr.add((prefix+ Literal("$"+crypto['price'], datatype=XSD.decimal), prefix+"checkedAt", Literal(crypto['checkedAt'])))

   payload = gr.serialize(format='turtle')
   headers = {
   'Content-Type': 'application/x-turtle;charset=UTF-8'
   }
   print(payload)
   response = requests.post('http://{}:{}/{}/statements?context=null'.format(app.config['server3_host'], app.config['server3_port'], app.config['server3_burl']), headers=headers, data=payload)

   if response.content == "":
      return payload + "was added to the database"
   else:
      return response.content



if __name__ == '__main__':
      app.run(host='0.0.0.0', debug=True, port=5000, ssl_context="adhoc")
