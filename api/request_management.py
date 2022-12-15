from dataclasses import dataclass, replace
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
                res = self.createUser()
                
            elif self.method == 'PUT':
                res = self.updateUser(self.path[1])
                
            elif self.method == 'DELETE':
                res = self.deleteUser(self.path[1])
                
            self.db.close_connection()            
            return res
    
    def getAllUsers(self):
        self.db.execute(self.db.selectAllStatement)
        res = self.db.CURSOR.fetchall()
        return ResponseHandler.list_tuple_to_class_dict(res)

    def getUser(self, id):
        self.db.execute(self.db.selectUUIDStatement % id)
        res = self.db.CURSOR.fetchone()
        return ResponseHandler.single_tuple_to_class_dict(res)
        
    def createUser(self):
        newUser = self.createUserClass()
        self.db.execute_data(self.db.insertStatement, newUser)
        self.db.commit()
        return self.getUser(newUser.uuid)

    def updateUser(self, id):
        self.db.execute(self.db.selectUUIDStatement % id)
        res = self.db.CURSOR.fetchone()
        self.db.CURSOR.close()
        self.db.CURSOR = self.db.CONN.cursor()
        user = User(*res[1:])
        self.updateUserItems(user)
        data = (user.username, user.name, user.email,
                user.sms, user.created, user.lastseen, user.uuid)
        self.db.execute_data(self.db.updateUserStatement, data)
        self.db.commit()
        return self.getUser(id)

    def deleteUser(self, id):
        self.db.execute(self.db.deleteUserStatement % id)
        self.db.commit()
        return {'uuid': id,
                'status': 'deleted'}



    def createUserClass(self):
        id = User.generate_uuid()
        newUser = User()
        newUser.uuid = id
        newUser = self.updateUserItems(newUser)
        return newUser
    
    def updateUserItems(self, user):
        for k,v in self.args.items():
            if k == 'created' or k == 'lastseen':
                user.__setattr__(k, int(v))
            else:
                user.__setattr__(k, v)
        return user