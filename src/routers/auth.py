from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.schemas.user import UserOut, UserRegister
from typing import Annotated
from src.repositories.user import UserRepository
from exceptions import UserAlreadyExistsException, UserNotFound
from src.models.user import User
from datetime import datetime, timezone


auth_router: APIRouter = APIRouter(
    prefix='/auth', 
    tags=['Аутентификация и Авторизация']
)



@auth_router.post('/register', status_code=201)
async def rigister_user(
    user: UserRegister,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserOut:

    exist_user: UserOut = await UserRepository.find_one_or_none(
        session=session, username=user.username
    )

    if exist_user:
        raise UserAlreadyExistsException
    current_date_time: datetime = datetime.now(timezone.utc)
    hashed_password: str = get_password_hash(user.password)
    new_user: User = await UserRepository.add(
        session=session, 
        username=user.username, 
        hashed_password=hashed_password, 
        registered_at=current_date_time, 
        )


    new_user_out: UserOut = UserOut.model_validate(new_user)
    return new_user_out



@auth_router.post('/login', status_code=200)
async def login_user(
    response: Response,
    user: UserRegister,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:

    user: UserOut = await authenticate_user(user.username, user.password, async_db=session)
    if not user:
        raise UserNotFound

    access_token = create_access_token({'sub': str(user.id)})

    response.set_cookie(
        'user_access_token', access_token, httponly=True
    )
    return access_token




@auth_router.post('/logout', status_code=200)
async def logout_user(
    response: Response,
    request: Request,
):
    cookies: str | None = request.cookies.get('user_access_token')
    if cookies:
        response.delete_cookie(key='user_access_token')