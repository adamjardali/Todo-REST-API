from config.database import Base 
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship 
from datetime import datetime
var_length = 100





class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key = True, index = True)
	name = Column(String(var_length),nullable = False)
	email = Column(String(var_length), nullable = False, unique = True)
	password = Column(String(var_length), nullable = False)
	created_at = Column(DateTime, nullable  = False, default = datetime.utcnow)
	tasks = relationship('Task', back_populates = 'creator')

class Task(Base):
	__tablename__ = 'tasks'
	id = Column(Integer,primary_key = True, index = True)
	title = Column(String(var_length),nullable = False, default = 'No title')
	description = Column(String(var_length),nullable = False, default = 'No description')
	user_id = Column(Integer,ForeignKey('users.id'))
	creator = relationship('User',back_populates = 'tasks')
	created_at = Column(DateTime, nullable  = False, default = datetime.utcnow)
	is_completed = Column(Boolean, nullable = False, default = False)