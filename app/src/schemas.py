from pydantic import BaseModel, EmailStr



#Cхема для регистрации на входе
class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str

#Cхема для регистрации на выходе
class UserRegisterOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

#Cхема для логина на входе
class UserLoginIn(BaseModel):
    email: EmailStr
    password: str

#Схема токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

#Cхема для логина на выходе
class UserLoginOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    token: Token



