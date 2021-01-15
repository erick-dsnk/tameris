import aiohttp
import asyncio
import json

class RequestHandler:
    def __init__(self, token: str):
        self.token = token
        self.url = 'https://discord.com/api'
    
    async def get(self, endpoint, extra_params = {}):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url + endpoint,
                headers={
                    'Authorization': f'Bot {self.token}'
                },
                params=extra_params
            ) as response:
                return response.status, await response.json()


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
                return response.status, await response.json()

    async def patch(self, endpoint, body):
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url=self.url + endpoint,
                headers={
                    'Authorization': f'Bot {self.token}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(body)
            ) as response:
                return response.status, await response.json()

    async def delete(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url=self.url + endpoint,
                headers={
                    'Authorization': f'Bot {self.token}',
                    'Content-Type': 'application/json'
                }
            ) as response:
                return response.status, await response.json()