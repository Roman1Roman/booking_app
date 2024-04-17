from datetime import timedelta, datetime
from app.config import settings
from fastapi import HTTPException
from pydantic import EmailStr
from app.exceptions import UserNotFound, InvalidCredentials
from passlib.context import CryptContext
from jose import jwt

from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    existing_user = await UsersDAO.find_one_or_none(email=email)
    if not existing_user:
        raise UserNotFound
    if not verify_password(password, existing_user.hashed_password):
        raise InvalidCredentials
    return existing_user

