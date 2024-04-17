from pydantic import BaseModel, EmailStr


class SUserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class SUserRegisterResponse(BaseModel):
    id: int
    email: EmailStr