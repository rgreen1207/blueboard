import datetime
import hashlib
import uuid

from dataclasses import dataclass

@dataclass
class User:
    __tablename__ = "users"
    __sa_dataclass_metadata_key__ = "sa"
    
    #pid: int = None
    uuid: str = None
    username: str = None
    name: str = None
    email: str = None
    sms: str = None
    created: int = None
    lastseen: int = None
    
    def generate_uuid():
        return hashlib.sha224(str(uuid.uuid4()).encode()).hexdigest() 
        
    def created_to_date(self):
        #assuming mm-dd-yyyy
        return datetime(
            month=self.created[0:2],
            day=self.created[2:4],
            year=self.created[4:]
            )
    
    def lastseen_to_date(self):
        #assuming mm-dd-yyyy
        return datetime(
            month=self.lastseen[0:2],
            day=self.lastseen[2:4],
            year=self.lastseen[4:]
        )

