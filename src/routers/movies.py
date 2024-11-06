from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from typing import Annotated
from src.models.favorite import Favorite
from src.models.movie import Movie
from src.schemas.user import UserOut
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp import ClientSession
from src.schemas.movie import MovieSchema, get_movie_schema
from src.utils.utils import fetch, get_aiohttp_session
from exceptions import MovieNotFound, MovieAlreadyExistsInFavorites, MovieNotInFavorites
from src.repositories.movie import MovieRepository
from src.repositories.favorite import FavoriteRepository


movies_router: APIRouter = APIRouter(
    prefix='/movies',
    tags=['Фильмы']
)



@movies_router.get('/search')
async def find_movies_by_keyword(
    query: Annotated[str, Query()],
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[ClientSession, Depends(get_aiohttp_session)]
) -> list[MovieSchema] | None:
    
    """
    Получение списка фильмов по ключевому слову
    """

    url: str = f'/api/v2.1/films/search-by-keyword?keyword={query}'
    res = await fetch(url=url, session=session)
    movie_info = res['films']
    if movie_info:
        result: list[MovieSchema] = get_movie_schema(result=movie_info, lst=True)
        return result
    return None




@movies_router.post('/favorites')
async def add_to_favorites(
    kinopoisk_id: int,
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    aiohttp_session: Annotated[ClientSession, Depends(get_aiohttp_session)]
) -> JSONResponse:

    """
    Добавление фильма в избранные
    """

    favorite_movie: Favorite = await FavoriteRepository.find_movie(session=session, user_id=user.id, filmId=kinopoisk_id)

    if favorite_movie:
        raise MovieAlreadyExistsInFavorites
    
    movie: Movie = await MovieRepository.find_one_or_none(session=session, filmId=kinopoisk_id)

    #В случае если такого фильма еще нет в базе, то добавляем его в бд, а затем в избранные
    if not movie:
        url: str = f'/api/v2.2/films/{kinopoisk_id}'
        result: dict[str, str] = await fetch(url=url, session=aiohttp_session)

        if not result:
            raise MovieNotFound

        movie_data: MovieSchema = get_movie_schema(result=result)
        movie: Movie = await MovieRepository.add(session=session, **movie_data.model_dump())

    await FavoriteRepository.add(session=session, user_id=user.id, movie_id=movie.id, film_id=movie.filmId)
    return JSONResponse(content={'message': 'Фильм добавлен в избранные.'})



@movies_router.get('/favorites')
async def get_favorite_movies(
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> list[MovieSchema]:
    
    """
    Получение списка избранных фильмов
    """

    movies: list[Movie] = await MovieRepository.get_favorite_movies(session=session, user_id=user.id)
    return movies



@movies_router.delete('/favorites/{kinopoisk_id}')
async def delete_favorite_movie(
    kinopoisk_id: int,
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> JSONResponse:
    
    """
    Удаление фильма из избранных
    """

    favorite_movie: Favorite = await FavoriteRepository.find_movie(session=session, filmId=kinopoisk_id, user_id=user.id)
    if favorite_movie:
        await FavoriteRepository.delete(session=session, id=favorite_movie.id)
        return JSONResponse(content={'message': 'Фильм удален из избранных'})
    else:
        raise MovieNotInFavorites



@movies_router.get('/{kinopoisk_id}')
async def find_movie_by_kinopoisk_id(
    kinopoisk_id: Annotated[int, Path(le=2000000000)],
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[ClientSession, Depends(get_aiohttp_session)]
) -> MovieSchema:
    
    """
    Поиск информации о фильме по его id в кинопоиске
    """

    url: str = f'/api/v2.2/films/{kinopoisk_id}'
    movie_info: dict[str, str] = await fetch(url=url, session=session)
    if movie_info:
        result: MovieSchema = get_movie_schema(result=movie_info)
        return result
    else:
        raise MovieNotFound