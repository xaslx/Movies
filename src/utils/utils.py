import aiohttp
import aiohttp.client_exceptions
from config import env_config



base_url: str = 'https://kinopoiskapiunofficial.tech'

headers: dict[str, str] = {
        'X-API-KEY': env_config.API_KEY,
        'Content-Type': 'application/json',
    }



async def get_aiohttp_session():
    async with aiohttp.ClientSession(base_url=base_url, headers=headers) as session:
        yield session




async def fetch(url: str, session: aiohttp.ClientSession):
    async with session.get(url=url) as response:
        if response.status == 200:
            return await response.json()
        return None