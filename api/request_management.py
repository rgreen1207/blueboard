from dataclasses import dataclass
from .db_handler import dbHandler
from .response_handler import ResponseHandler
from models import User

@dataclass
class RequestManagement:
    path: str
    method: str
    args: dict
    
    db = dbHandler()
    
    def handle_request(self):
        print("Request Management class: ", self)
        if self.method not in ['GET', 'POST', 'PUT', 'DELETE']:
            return "Not a valid method"
        else:
            self.db.connect()
            res = {} 
            
            if self.method == 'GET':
                if(len(self.path) == 1 and self.path[0] == 'users'):
                    res =  self.getAllUsers()
                else: 
                    res = self.getUser(self.path[1])
                                        
            elif self.method == 'POST':
                res = self.createUser(self.args)
                
            elif self.method == 'PUT':
                res = self.updateUser(self.getUserId())
                
            elif self.method == 'DELETE':
                res = self.deleteUser(self.path[1])
                
            self.db.close_connection()            
            return res
    
    def getAllUsers(self):
        self.db.execute(self.db.selectAllStatement)
        res = self.db.CURSOR.fetchall()
        res = ResponseHandler.list_tuple_to_class_dict(res)
        return res

    def getUser(self, id):
        self.db.execute(self.db.selectUUIDStatement % id)
        res = self.db.CURSOR.fetchone()
        res = ResponseHandler.single_tuple_to_class_dict(res)
        return res

    def createUser(self, argsList):
        newUser = self.createUserClass(argsList)
        self.db.execute_addition(self.db.insertStatement, newUser)
        self.db.commit()
        res = self.getUser(newUser.uuid)
        return res

    def updateUser(self, id, argsList):
        pass
        return self.getUser(id)

    def deleteUser(self, id):
        self.db.execute(self.db.deleteUserStatement % id)
        self.db.commit()
        return {'uuid': id,
                'status': 'deleted'}

    def createUserClass(self, argsList):
        id = User.generate_uuid()
        newUser = User()
        newUser.uuid = id
        for k,v in argsList.items():
            if k == 'created' or k == 'lastseen':
                newUser.__setattr__(k, int(v))
            else:
                newUser.__setattr__(k, v)
        return newUser