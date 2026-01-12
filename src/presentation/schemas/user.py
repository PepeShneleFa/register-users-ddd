from pydantic import BaseModel

class AuthResult(BaseModel):
    status: str
    message: str
    access_token: str

class UserAuthRequest(BaseModel):
    username: str
    password: str

class ProfileAuthRequest(BaseModel):
    age: int
    name: str
    city: str

class ProfileAuthResult(BaseModel):
    status: str
    message: str

class PostAuthRequest(BaseModel):
    title: str
    content: str

class PostAuthResult(BaseModel):
    status: str
    message: str

class GetPostsByID(BaseModel):
    user_id: str