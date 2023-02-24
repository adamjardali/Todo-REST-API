from fastapi import  Depends, HTTPException, status, Response
from config import models,oauth2, database
import schemas
from sqlalchemy.orm import Session
from config.hashing import Hash

class User:
	def register_user(user:schemas.UserIn, db:Session):
		hashed_password = Hash.bcrypt(user.password)
		user.password = hashed_password
		is_unique_email = db.query(models.User).filter(models.User.email == user.email)
		if is_unique_email.first():
			raise HTTPException(status_code =  409, detail = f"Email {user.email} is taken by another user")

		new_user = models.User(**user.dict())
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
		return new_user

	def get_user_by_id(id: int, db: Session):
		user = db.query(models.User).filter(models.User.id == id).first()
		if not user:
			raise HTTPException(status_code = 404, detail =  f"User with id {id} is not found")
		return user

	def delete_user(id:int, db:Session, current_user : int):
		user = db.query(models.User).filter(models.User.id == id)
		if not user.first():
			raise HTTPException(status_code = 404, detail = f"User with id {id} is not found")
		if user.first().id != current_user.id:
			raise HTTPException(status_code = 403, detail = f"Not authorized to perform requested action")
		user.delete(synchronize_session = False)
		db.commit()
		return Response(status_code = 204)

	def update_user(id: int, new_user: schemas.UserIn,db:Session, current_user : int):
		user = db.query(models.User).filter(models.User.id == id)
		if not user.first():
			raise HTTPException(status_code = 404, detail = f"User with id {id} is not found")
		if user.first().id != current_user.id:
			raise HTTPException(status_code = 403, detail = f"Not authorized to perform requested action")
		user.update(new_user.dict(),synchronize_session = False)
		db.commit()
		return user.first()
