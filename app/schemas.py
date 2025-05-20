###(Pydantic-схемы для валидации запросов)

import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import enum


###схемы для логина и токена
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str

 ###роль клиента  
class UserRole(str, enum.Enum):
    client = "client"
    master = "master"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str    

class MasterProfileCreate(BaseModel):
    user_id : int
    specialization: str
    description: Optional[str] = None

class OrderCreate(BaseModel):
    master_id: int
    description: str


class UserRead(BaseModel):
    # Схема для данных пользователя
    id: int                
    name: str              
    email: EmailStr        

    model_config = ConfigDict(from_attributes=True)


class MasterProfileRead(BaseModel):
    # Схема для профиля мастера
    id: int               
    specialization: str    
    description: Optional[str]  
    user: UserRead          

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    # Схема для данных о заказе
    id: int               
    description: str     
    client_id: int       
    master_id: int       
    created_at: datetime.datetime  

    model_config = ConfigDict(from_attributes=True)