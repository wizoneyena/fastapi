import datetime
from app import oauth2
from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

#Create new user
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	#hash password
	hashed_pwd = utils.hash(user.password)
	user.password = hashed_pwd
	#Creating new user
	new_user = models.Users(**user.dict())

	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user

#Get user data by ID
@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
	user = db.query(models.Users).filter(models.Users.id == id).first()
	if not user or user.deleted == True:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id -{id}- was not found")
	return user

#Delete User
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	user_query = db.query(models.Users).filter(models.Users.id == id)
	user = user_query.first()

	if user == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with id: -{id}- was not found")
	elif user.deleted == True:
		raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"user with id: -{id}- was not found")

	if user.id != current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized for this action")

#Update deleted and deleted_at values
	user.deleted = True
	user.deleted_at = datetime.datetime.now()
	db.commit()

	return Response(status_code = status.HTTP_204_NO_CONTENT)