from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config import database , models, hashing, oauth2

get_db = database.get_db

router = APIRouter(
		tags = ['Authentication']
	)

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db :Session = Depends(get_db)):
	user = db.query(models.User).filter(user_credentials.username == models.User.email).first()

	if not user: 
		raise HTTPException(status_code = 403, detail = "Invalid credentials")
	
	if 	not hashing.Hash.verify(user.password,user_credentials.password):
		raise HTTPException(status_code = 403, detail = "Invalid credentials")
	
	access_token = oauth2.create_access_token({'user_id':user.id})
	return {'access_token':access_token, 'token_type':'bearer'}

