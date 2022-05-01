import requests
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import XSD

url = "http://192.168.0.186:8080//rdf4j-server/repositories/grafexamen"

payload = "construct {?s ?p ?o} where {?s ?p ?o}"
headers = {
  'Content-Type': 'application/sparql-query'
}
gr = Graph()
response = requests.request("POST", url, headers=headers, data=payload)

gr.parse(response.content)

gr.namespace_manager.bind('', URIRef("http://grafexamen#"))

print(gr.serialize(format='turtle'))