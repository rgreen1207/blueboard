import json
from models import User
from api import dbHandler
from dataclasses import astuple

def createUsers():
    db = dbHandler()
    db.connect()
    userList = []
    with open('data.json') as data:
        users = json.loads(data.read())
        for i, user in enumerate(users):
            fields = user['fields']
            userList.append(User( 
                     User.generate_uuid(), 
                     fields['username'], 
                     fields['name'],
                     fields['email'],
                     fields['sms'],
                     fields['created'],
                     fields['lastseen']
                     ))
            
        
        
    insertStatement = ("INSERT INTO users (uuid, username, name, email, sms, created, lastseen) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    for i in userList:
        db.CURSOR.execute(insertStatement, astuple(i))
        #db.commit()
    db.close_connection()
        
        
if __name__ == '__main__':
    createUsers()