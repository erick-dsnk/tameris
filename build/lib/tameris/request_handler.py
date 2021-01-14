import aiohttp
import asyncio
import json

class RequestHandler:
    def __init__(self, token: str):
        self.token = token
        self.url = 'https://discord.com/api'
    
    async def get(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url + endpoint,
                headers={
                    'Authorization': f'Bot {self.token}'
                }
            ) as response:
                return await response.json()


    async def post(self, endpoint, body):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.url + endpoint,
                headers={
                    'Authorization': f'Bot {self.token}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(body)
            ) as response:
                return await response.json()

