from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ── Request schemas ─────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Response schemas ────────────────────────────────────────

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    email: str
    username: str
    createdAt: datetime = Field(validation_alias="created_at")


class AuthResponse(BaseModel):
    token: str
    user: UserRead
