from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#Defining our posts table in a class
class Posts(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key = True, nullable = False)
	title = Column(String, nullable = False)
	content = Column(String, nullable = False)
	published = Column(Boolean, server_default = 'TRUE', nullable = False)
	created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
 
	#Automatically fetch data from Users table without FK
	owner = relationship("Users")
 

#Define our users table
class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True, nullable = False)
	email = Column(String, nullable = False, unique = True)
	password = Column(String, nullable = False)
	created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
	#Implement Soft Delete
	deleted = Column(Boolean, nullable = False, default = False)
	deleted_at = Column(TIMESTAMP(timezone = True), nullable = True)

#Define Likes table
class Likes(Base):
    __tablename__ = "likes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)