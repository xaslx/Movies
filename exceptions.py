from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)




class MovieNotFound(BaseException):
    status_code = 404
    detail = "Фильм не найден"


class MovieAlreadyExistsInFavorites(BaseException):
    status_code = 409
    detail = "Фильм уже находится в избранных"


class MovieNotInFavorites(BaseException):
    status_code = 404
    detail = "Фильм не находится в избранных"


class NotAccessError(BaseException):
    status_code = 403
    detail = "Недостаточно прав"


# Пользователи
class UserAlreadyExistsException(BaseException):
    status_code = 409
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BaseException):
    status_code = 401
    detail = "Неверный email или пароль"


class IncorrectEmailOrPasswordExceptionNotEn(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Email или пароль должны быть на английском"


class UserNotFound(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь не найден"


class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED


# JWT token
class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"