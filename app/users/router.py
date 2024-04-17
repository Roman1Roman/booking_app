from fastapi import APIRouter, HTTPException, Response, Depends
from app.exceptions import UserAlreadyExists
from app.users.models import Users
from app.users.schemas import SUserRegisterRequest, SUserRegisterResponse
from app.users.dao import UsersDAO
from app.users import auth
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users | Пользователи']
)

@router.post('/register')
async def register_user(user_data: SUserRegisterRequest):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExists
    hashed_password = auth.get_password_hash(user_data.password)
    new_user = await UsersDAO.insert_row(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise HTTPException(status_code=400, detail='Failed to register user')


@router.post('/login')
async def login_user(response: Response, user_data: SUserRegisterRequest):
    existing_user = await auth.authenticate_user(user_data.email, user_data.password)
    access_token = auth.create_access_token(data={'sub': str(existing_user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')
    return {'message': 'Logged out'}


@router.get('/current')
async def get_current_user(user: Users = Depends(get_current_user)) -> SUserRegisterResponse:
    return user


@router.get('/all')
async def get_all_users():
    return await UsersDAO.find_all()
