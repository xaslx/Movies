from fastapi import FastAPI
from src.routers.auth import auth_router
from src.routers.profile import profile_router
from src.routers.movies import movies_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware




app: FastAPI = FastAPI()

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(movies_router)


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run(app)