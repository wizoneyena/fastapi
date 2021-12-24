from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, utils, oauth2, schemas


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model = schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_creds.username).first()
    
    if not user or user.deleted == True:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    #Create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "email": user.email})
    refresh_token = oauth2.create_refresh_token(data = {"user.id": user.id})

    return {"access_token": access_token, "access_token_type": "Bearer", "refresh_token": refresh_token, "refresh_token_type": "Token"}


#Refresh Token route
@router.post('/refresh', response_model = schemas.Token)
def refresh(request: Request, db: Session = Depends(database.get_db)):
    token = request.headers.get('refresh_token')

    x = oauth2.verify_refresh_token(token, Exception)
    user_id = oauth2.get_user_from_refreshtoken(token)
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not user or user.deleted == True:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id, "email": user.email})
    refresh_token = oauth2.create_refresh_token(data = {"user.id": user.id})

    return {"access_token": access_token, "access_token_type": "Bearer", "refresh_token": refresh_token, "refresh_token_type": "Token"}

#TODO Redirect Logout