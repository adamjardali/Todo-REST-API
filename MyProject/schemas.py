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

class TaskIn(BaseModel):
	title: str | None = None
	description: str | None = None
	is_completed: bool| None = None
	class Config():
		orm_mode = True
class TaskOut(BaseModel):
	title: str | None = None
	description: str | None = None
	is_completed : bool | None = None
	created_at: datetime
	class Config():
		orm_mode = True

class TokenData(BaseModel):
	id: str | None = None
