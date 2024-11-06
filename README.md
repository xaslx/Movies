# Movie

Это веб-приложение, использующее Kinopoisk API Unofficial для получения информации о фильмах. 
Приложение поддерживает аутентификацию и авторизацию с использованием JWT токенов, а также предоставляет возможность поиска фильмов по их Kinopoisk ID и ключевым словам. 
Пользователи могут добавлять фильмы в избранные и удалять их оттуда.

## Технологии

- **FastAPI** - для создания веб-приложения
- **PostgreSQL** - для хранения данных
- **SQLAlchemy** - для работы с базой данных
- **aiohttp** - для асинхронных HTTP запросов
- **JWT** - для аутентификации
- **asyncio** - для асинхронного программирования

## Установка

## Настройка

Перед запуском приложения убедитесь, что вы создали файл `.env` в корневой директории проекта и заполнили его следующими переменными:

```plaintext
LOG_LEVEL=INFO - Уровень логирования

Подключение к базе данных
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres

SECRET_KEY=ваш_секретный_ключ для JWT
SECRET_ALGORITHM=для JWT

API_KEY=API ключ можно получить на https://kinopoiskapiunofficial.tech/
```

### Запуск без Docker
  
   ```
  git clone https://github.com/xaslx/Movies.git
  cd movies
  python -m venv venv
  venv/Scripts/activate
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```

### Запуск с Docker
  ```docker compose up --build```


