from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserSummary(BaseModel):
    id: str
    name: str
    email: EmailStr


class AuthResponse(BaseModel):
    user: UserSummary
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str
