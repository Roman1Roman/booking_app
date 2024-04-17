from datetime import datetime
from app.exceptions import TokenNotFound, InvalidToken, TokenExpired, UserNotFound
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenNotFound
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise InvalidToken
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpired
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserNotFound
    user = await UsersDAO.find_by_id(id=int(user_id))
    if not user:
        raise UserNotFound
    return user