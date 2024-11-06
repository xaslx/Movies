from pydantic import BaseModel, ConfigDict




class Country(BaseModel):
    country: str

class Genre(BaseModel):
    genre: str

class MovieSchema(BaseModel):
    filmId: int | None
    nameRu: str | None
    type: str | None
    year: str | None
    description: str | None
    filmLength: str | None
    countries: list[Country | None] | None
    genres: list[Genre | None] | None
    rating: str | None

    model_config = ConfigDict(from_attributes=True)



def create_movie_schema(data: dict[str, str]) -> MovieSchema:
        dat = data.get('nameOriginal')
        return MovieSchema(
            filmId=data.get('filmId') or data.get('kinopoiskId'),
            nameRu=data.get('nameRu') or data.get('nameOriginal'),
            type=data.get('type'),
            year=str(data.get('year')),
            description=data.get('description'),
            filmLength=str(data.get('filmLength')),
            countries=[Country(**country) for country in data.get('countries', [])],
            genres=[Genre(**genre) for genre in data.get('genres', [])],
            rating=str(data.get('rating') or data.get('ratingKinopoisk'))
        )


def get_movie_schema(result: dict[str, str], lst: bool | None = None) -> MovieSchema | list[MovieSchema]:
    if lst:
        return [create_movie_schema(f) for f in result]
    return create_movie_schema(result)