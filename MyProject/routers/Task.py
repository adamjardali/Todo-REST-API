from fastapi import APIRouter, Depends, HTTPException, status, Response
from config import models, oauth2, database
import schemas
from sqlalchemy.orm import Session
from typing import List
from Repositories.Task import  Task

router = APIRouter(
	prefix = '/tasks',
	tags = ['Tasks']
	)

get_db = database.get_db

@router.post('/{user_id}',response_model = schemas.TaskOut)
def create_new_task(user_id:int,task: schemas.TaskIn, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
	return Task.create_new_task(user_id,task,db,current_user)


@router.get('/{user_id}/tasks', response_model = List[schemas.TaskOut])
def get_all_tasks(user_id:int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
	return Task.get_all_tasks(user_id,db,current_user)

@router.get('/{id}/sortedtasks', response_model = List[schemas.TaskOut])
def get_sorted_tasks(id:int,db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),):
	return Task.get_sorted_tasks(id,db,current_user)

@router.get('/{id}', response_model = schemas.TaskOut)
def get_task_by_id(id:int, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
	return Task.get_task_by_id(id,db,current_user)

@router.get('/{id}/completed', response_model = List[schemas.TaskOut])
def get_completed_tasks(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	return Task.get_completed_tasks(id,db,current_user)

@router.get('/{id}/pagintation', response_model = List[schemas.TaskOut])
def get_custom_tasks(id : int,skip: int = 0, limit : int = 10, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
	return Task.get_custom_tasks(id,skip,limit,db,current_user)

@router.put('/update/{user_id}/{task_id}', response_model = schemas.TaskOut)
def update_task(user_id:int, task_id:int, new_task: schemas.TaskIn,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	return Task.update_task(user_id,task_id,db,current_user)


@router.delete('/update/{user_id}/{task_id}')
def delete_task(user_id:int, task_id:int,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	return Task.delete_task(user_id,task_id,db,current_user)


