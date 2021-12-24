from passlib.context import CryptContext



#Setting default hashing algorithm
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#Function to hash password
def hash(password: str):
	return pwd_context.hash(password)

#Verify if password is correct
def verify(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
