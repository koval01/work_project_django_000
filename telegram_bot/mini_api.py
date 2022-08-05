from aiohttp import ClientSession
import os


class Api:
    def __init__(self, login: str) -> None:
        self.host:  str = os.getenv("APP_HOST")
        self.key:   str = os.getenv("API_KEY")
        self.login: str = login

    async def _request(self) -> dict:
        async with ClientSession() as session:
            async with session.post("%s%s" % (self.host, "create_user"), json={
                "login": self.login,
                "key": self.key
            }
            ) as response:
                return response.json() \
                    if response.status >= 200 < 300 \
                    else {"error": True}

    async def create_user(self) -> dict:
        return await self._request()
