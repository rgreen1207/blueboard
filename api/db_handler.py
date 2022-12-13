import mysql.connector as mysql

from dataclasses import dataclass

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
    
    def connect(self):
        self.CONN = mysql.connect(host=self.HOST, database=self.DATABASE, user=self.USER, password=self.PASSWORD, port=self.PORT)
        self.CURSOR = self.CONN.cursor()
        
        print("Connected to:", self.CONN.get_server_info())
        
    def execute(self):
        pass
    
    def commit(self):
        pass
    
    def close_connection(self):
        self.CONN.close()
    
    