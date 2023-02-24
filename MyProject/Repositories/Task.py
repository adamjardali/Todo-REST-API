from fastapi import HTTPException, status, Response
from config import models, oauth2, database
import schemas
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import and_, or_, not_

class Task:
	def create_new_task(user_id:int,task: schemas.TaskIn, db:Session, current_user:int):
		if user_id != current_user.id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		new_task = models.Task(user_id = current_user.id,**task.dict())
		db.add(new_task)
		db.commit()
		db.refresh(new_task)
		return new_task

	def get_all_tasks(user_id:int,db:Session,current_user : int):
		if user_id != current_user.id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		tasks = db.query(models.Task).filter(user_id == models.Task.user_id).all()
		if not tasks:
			raise HTTPException(status_code = 204, detail = "No Tasks")
		return tasks

	def get_sorted_tasks(id:int,db:Session,current_user : int):
		if current_user.id != id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		tasks = db.query(models.Task).filter(id == models.Task.user_id).order_by(models.Task.is_completed.desc()).all()
		if not tasks:
			raise HTTPException(status_code = 204, detail = "No Tasks")
		return tasks
	def get_task_by_id(id:int, db:Session, current_user : int):
		task = db.query(models.Task).filter(id == models.Task.id).first()
		if not task:
			raise HTTPException(status_code = 404,detail = f"Task with id {id} is not found")
		if current_user.id != task.user_id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")	
		return task

	def get_completed_tasks(id:int, db:Session, current_user:int):
		if current_user.id != id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		tasks = db.query(models.Task).filter(and_(id == models.Task.user_id,models.Task.is_completed == True)).all()
		if not tasks:
			raise HTTPException(status_code = 204, detail = "No Tasks are completed")
		return tasks

	def get_custom_tasks(id : int,skip: int, limit : int, db:Session, current_user : int):
		if current_user.id != id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		tasks = db.query(models.Task).limit(limit).offset(skip).all()
		return tasks

	def update_task(user_id:int, task_id:int, new_task: schemas.TaskIn,db:Session, current_user: int):
		if current_user.id != user_id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		task = db.query(models.Task).filter(and_(task_id == models.Task.id, models.Task.user_id == user_id))
		if not task.first():
			raise HTTPException(status_code = 404, detail = f'Task with id {task_id} is not found.')
		task.update(new_task.dict(),synchronize_session = False)
		db.commit()
		return task.first()

	def delete_task(user_id:int, task_id:int,db:Session, current_user: int):
		if current_user.id != user_id:
			raise HTTPException(status_code = 403, detail = "You dont have access to this resource")
		task = db.query(models.Task).filter(and_(task_id == models.Task.id, models.Task.user_id == user_id))
		if not task.first():
			raise HTTPException(status_code = 404, detail = f'Task with id {task_id} is not found.')
		task.delete(synchronize_session = False)		
		db.commit()
		return Response(status_code = 204)