from pydantic import BaseSettings

#Pydantic model for environment variables -> Checks system (case insensitive) for env variables if no default set
class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    secret_key_refresh: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    
    #Use .env file if variables are not set on the system (for development)
    class Config:
        env_file = ".env"
    
    
#Instance for accessing env variables   
settings = Settings()    

