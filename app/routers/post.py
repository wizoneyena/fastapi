from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=['Posts'])

#Get all posts from the database

@router.get("/", response_model = List[schemas.PostOut])
#Adding dependecies and query parameters
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str]= ""):
    #Allow returning all posts
 	#Return only posts created by the user	
	#posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
	#return posts
	
	#Return Posts with likes and filter query
	results = db.query(models.Posts, func.count(models.Likes.post_id).label("likes")).join(models.Likes, models.Likes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).all()
	print(results)
	return results

#Create new post
#TODO add middleware (interceptor) for refresh token handling
#TODO Verify refresh token
#TODO Implement redirecting
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	new_post = models.Posts(owner_id = current_user.id, **post.dict())
 
	db.add(new_post)
	db.commit()
	db.refresh(new_post)

	return new_post


#Get specific post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	post = db.query(models.Posts, func.count(models.Likes.post_id).label("likes")).join(models.Likes, models.Likes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()
 
	if not post:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {-id}- was not found")
	return post


#Update Post
@router.put("/{id}", response_model=schemas.Response)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Posts).filter(models.Posts.id == id)
	post = post_query.first()

	if post == None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: -{id}- was not found")
	
	if post.owner_id != oauth2.get_current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized for this action")

	post_query.update(updated_post.dict(), synchronized_session = False)
	db.commit()
	return post_query.first()


#Delete specific post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Posts).filter(models.Posts.id == id)
	post = post_query.first()

	if post == None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: -{id} was not found")

	if post.owner_id != current_user.id:
		raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized for this action")

	post_query.delete(synchronize_session = False)
	db.commit()

	return Response(status_code = status.HTTP_204_NO_CONTENT)
