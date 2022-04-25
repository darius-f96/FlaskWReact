from crypt import methods
from unicodedata import name
from classes.Employee import Employees
from classes.Organization import Organizations, Organization
from flask import Flask, jsonify, request
import requests, json
#graphql libraries
from gql import Client, gql
from gql.dsl import DSLSchema, DSLQuery, dsl_gql
from gql.transport.requests import RequestsHTTPTransport

app = Flask(__name__)

app.config['server1_host'] = "localhost"
app.config['server1_port'] = '4000'

app.config['server2_host'] = "localhost"
app.config['server2_port'] = '3000'

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
   
   pass

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


if __name__ == '__main__':
      app.run(host='0.0.0.0', debug=True, port=5000, ssl_context="adhoc")
