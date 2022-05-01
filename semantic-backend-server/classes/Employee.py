import json, uuid
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import XSD

prefix = URIRef("http://grafexamen#")

class Employee:
    def __init__(self, firstname, lastname, age, orgId, dbId) -> None:
        self.__firstname = firstname
        self.__lastname = lastname
        self.__orgId = orgId
        self.__age = age
        if dbId != "":
            self.__id = dbId
        else:
            self.__id = str(uuid.uuid1())
    
    def toJson(self):
       return {'id' : self.__id, 
            'firstname' : self.__firstname, 
            'lastname' : self.__lastname,
            'organizationId' : self.__orgId,
            'age' : self.__age}

    def getFullName(self):
        return self.__firstname + " " + self.__lastname
    
    def addToGraph(self, gr):

        gr.add((prefix+self.__id, prefix+"hasFirstName", Literal(self.__firstname, datatype=XSD.string)))
        gr.add((prefix+self.__id, prefix+"hasLastName", Literal(self.__lastname, datatype=XSD.string)))
        gr.add((prefix+self.__id, prefix+"hasAge", Literal(self.__age, datatype=XSD.integer)))
        gr.add((prefix+self.__id, prefix+"employeeOf", prefix+self.__orgId))


class Employees:
    def __init__(self) -> None:
        self.__emp = []
    def addEmp(self, str):
        if not self.exists(str):
            if 'firstname' in str and 'lastname' in str and 'organizationId' in str:
                if not 'age' in str:
                    str['age'] = 0
                if 'id' in str:
                    self.__emp.append(Employee(str['firstname'], str['lastname'], str['age'], str['organizationId'], str['id']))
                else:
                    self.__emp.append(Employee(str['firstname'], str['lastname'], str['age'], str['organizationId'], ""))

    def getAll(self):
        return self.__emp
    
    def getAllJson(self):
        result = []
        for emp in self.__emp:
            result.append(emp.toJson())
            
        return result
    
    def exists(self, verify_obj):
        for verify in self.__emp:
            if verify.getFullName() == (verify_obj['firstname'] + " " + verify_obj['lastname']):
                return True
        return False
