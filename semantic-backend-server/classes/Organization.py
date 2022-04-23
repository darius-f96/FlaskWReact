import json
import uuid
from xmlrpc.client import Boolean, boolean

class Organization:
    def __init__(self, name, cui, dbId) -> None:
        self.__name = name
        self.__cui = cui
        self.__dbId = dbId
        self.__id = str(uuid.uuid1())
    
    def toJson(self):
       return {'id' : self.__id, 
            'name' : self.__name, 
            'cui' : self.__cui}
    
    def getName(self):
        return self.__name
    
    def getDbId(self):
        return self.__dbId
    
    def verifyExistance(self, verify):
        if self.__name == verify:
            return True
        return False

class Organizations:
    def __init__(self) -> None:
        self.__org = []
    def addOrg(self, str):
        if 'name' in str and 'cui' in str:
            if 'id' in str:
                self.__org.append(Organization(str['name'], str['cui'], str['id']))
            else:
                self.__org.append(Organization(str['name'], str['cui'], ""))

    def getAll(self):
        return self.__org
    
    def exists(self, verify_obj):
        for verify in self.__org:
            if verify.getName() == verify_obj['name']:
                return True
        return False
    
    def getIdByName(self, verify_obj):
        if 'organizationName' in verify_obj:
            for verify in self.__org:
                if verify.verifyExistance(verify_obj['organizationName']):
                    return verify.getDbId()
        return 0
