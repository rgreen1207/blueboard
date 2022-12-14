import mysql.connector as mysql

from dataclasses import dataclass, astuple

@dataclass
class dbHandler():
    HOST:str = "usersdb.c5s40hx7qswm.us-west-2.rds.amazonaws.com"
    DATABASE: str = "sys"
    TABLE: str = "users"
    USER: str = "admin"
    PASSWORD: str = "password"
    PORT: int = 3306
    CONN: object = None
    CURSOR: object = None
    
    insertStatement = ("INSERT INTO users (uuid, username, name, email, sms, created, lastseen) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    
    selectAllStatement = ("SELECT * FROM users")
    
    selectUUIDStatement = ("SELECT * FROM users WHERE uuid = '%s'")
    
    deleteUserStatement = ("DELETE FROM users WHERE uuid = '%s'")
    
    updateUserStatement = ("UPDATE users SET")
    
    def connect(self):
        try:
            self.CONN = mysql.connect(host=self.HOST, 
                                      database=self.DATABASE, 
                                      user=self.USER, 
                                      password=self.PASSWORD, 
                                      port=self.PORT)
            self.CURSOR = self.CONN.cursor()
            print("Connected to:", self.CONN.get_server_info())
        except mysql.connection.Error as err:
            print(err)
        
    def execute(self, statement):
        self.CURSOR.execute(statement)
            
    def execute_addition(self, statement, data):
        print(statement)
        print(astuple(data))
        self.CURSOR.execute(statement, astuple(data))
        
    def commit(self):
        self.CONN.commit()
    
    def close_connection(self):
        self.CONN.close()
        print("Closed connection to database.")
