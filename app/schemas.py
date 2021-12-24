from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#Define what a post should look like with pydantic
class PostBase(BaseModel):
        title: str
        content: str
        published: bool = True

#Extending PostBase for later uses with inheritance
class PostCreate(PostBase):
	pass

#Response when querying user 
class UserResponse(BaseModel):
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		orm_mode = True

#Define what a response should look like (Post)
class Response(PostBase):
	id: int
	created_at: datetime
	owner_id: int
	#Return a User also
	owner: UserResponse

	#Need this so pydantic can convert from SQLAlchemy model to dict
	class Config:
		orm_mode = True

#Schema for query with like
class PostOut(PostBase):
	Post: Response
	likes: int


#Schema for creating user
class UserCreate(BaseModel):
	email: EmailStr
	password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
	access_token: str
	access_token_type: str
	refresh_token: str
	refresh_token_type: str
    
class TokenData(BaseModel):
	id: Optional[str]
	email: Optional[EmailStr]


#Schema for Likes 
class Like(BaseModel):
	post_id: int
	type: conint(le=1)