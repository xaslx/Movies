from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from typing import Annotated

from src.schemas.user import UserOut



profile_router: APIRouter = APIRouter(
    prefix='/profile',
    tags=['Профиль']
)



@profile_router.get('')
async def get_my_profile(user: Annotated[UserOut, Depends(get_current_user)]) -> UserOut:
    return user