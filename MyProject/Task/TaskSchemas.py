from pydantic import BaseModel
from datetime import datetime

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