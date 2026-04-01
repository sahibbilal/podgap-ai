from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Shared schemas for sources
class Source(BaseModel):
    name: str  # e.g., "Google Trends", "Reddit", "YouTube"
    url: str   # Link to the source
    icon: str  # Emoji or icon representation
