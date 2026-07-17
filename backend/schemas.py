from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    current_class: Optional[int] = None
    country: Optional[str] = None
    interests: Optional[List[str]] = []


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    email: EmailStr
    current_class: Optional[int] = None
    country: Optional[str] = None
    interests: List[str] = []
    