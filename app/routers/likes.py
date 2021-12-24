from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/like")

#Endpoint for liking a post
@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session=Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #Check if user liked the post already
    like_query = db.query(models.Likes).filter(models.Likes.post_id == like.post_id, models.Likes.user_id == current_user.id)
    found_like = like_query.first()
    
    #Liking
    if(like.type == 1):
        if found_like:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} already liked this post")
        new_like = models.Likes(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"msg":"Like sent"}
        
    #Remove like
    else:
        if not found_like:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cant remove non-existent like")
        like_query.delete(synchronize_session = False)
        db.commit()
        return {"msg":"Like deleted"}
        