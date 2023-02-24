from pydantic import BaseModel
from datetime import datetime

class UserIn(BaseModel):
	name:str 
	password: str
	email:str
	class Config():
		orm_mode = True
class UserOut(BaseModel):
	name: str
	email: str 
	created_at : datetime
	class Config():
		orm_mode = True