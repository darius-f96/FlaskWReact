import json

import uuid
class Employee:
    def __init__(self, firstname, lastname, age, orgId, dbId) -> None:
        self.__firstname = firstname
        self.__lastname = lastname
        self.__id = uuid.uuid1()
        self.__orgId = orgId
        self.__age = age
        self.__dbId = dbId
    
    def toJson(self):
       return {'id' : self.__id, 
            'firstname' : self.__firstname, 
            'lastname' : self.__lastname,
            'organizationId' : self.__orgId,
            'age' : self.__age}

    def getFullName(self):
        return self.__firstname + " " + self.__lastname

class Employees:
    def __init__(self) -> None:
        self.__emp = []
    def addEmp(self, str):
        if 'firstname' in str and 'lastname' in str and 'organizationId' in str:
            if not 'age' in str:
                str['age'] = 0
            if 'id' in str:
                self.__emp.append(Employee(str['firstname'], str['lastname'], str['age'], str['organizationId'], str['id']))
            else:
                self.__emp.append(Employee(str['firstname'], str['lastname'], str['age'], str['organizationId'], ""))

    def getAll(self):
        return self.__emp
    
    def exists(self, verify_obj):
        for verify in self.__emp:
            if verify.getFullName() == (verify_obj['firstname'] + " " + verify_obj['lastname']):
                return True
        return False
