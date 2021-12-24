import requests
from starlette.middleware.base import BaseHTTPMiddleware

from .database import engine
from .routers import post, user, auth, likes
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

#Middleware / Interceptor for all routes -> Handle token logic
class RefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code == 401:
            if request.headers.get('refresh_token'):
                requests.post("http://localhost:8000/refresh/", headers = {'refresh_token': f'{request.headers.get("refresh_token")}'})
                return response
        return response
        
#Create our DB defined in models.py
#models.Base.metadata.create_all(bind = engine)

app = FastAPI()


#Allow CORS
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins,
                   allow_methods = ["*"],
                   allow_credentials = True,
                   allow_headers = ["*"],)

app.add_middleware(RefreshTokenMiddleware)


#Include routes from post.py and user.py
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)

#Default page
@app.get("/")
def root():
	return{"msg":"root"}


