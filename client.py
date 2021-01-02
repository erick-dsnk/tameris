import asyncio
import sys
import requests
import websockets
import json

from models.member import Member

from websockets.exceptions import PayloadTooBig

class Client:
    def __init__(self, bot_token: str):
        self.token = bot_token

        self.is_connected: bool = False
        self.user: Member = None
        self.intents: int = 513

        resp = requests.get(
            'https://discord.com/api/gateway/bot',
            headers={
                'authorization': f'Bot {self.token}'
            }
        ).json()

        self.__ws_url = resp['url'] + "?v=6&encoding=json"
        self.__recommended_shards = resp['shards']
        self.ws = None

        self.session_id = None

        self.__heartbeat_interval = None

        self.__data = None

        self.loop = asyncio.get_event_loop()

    async def connect(self):
        self.ws = await websockets.connect(uri=self.__ws_url)

        print('connected')

        self.loop.create_task(self.__receive_data())

        identify_payload = {
            'op': 2,
            'd': {
                'token': self.token,
                'intents': 513,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'tameris',
                    '$device': 'tameris'
                },
                'presence': {
                    'status': 'online',
                    'afk': False
                }
            }
        }

        await self.__send_data(payload=identify_payload)

        print('sent identify')

        self.loop.create_task(self.__heartbeat())


    async def __receive_data(self):
        while True:
            self.__data = await self.ws.recv()

            print('received data')

            print(self.__data)

            self.__data = json.loads(self.__data)

            if self.__data['op'] == 10:
                self.__heartbeat_interval = float(self.__data['d']['heartbeat_interval'] / 1000)

            self.session_id = self.__data['s']

            data = self.__data['d']

            if self.__data['t'] == 'READY':
                self.user = Member(
                    name=data['user']['name'],
                    discriminator=data['user']['discriminator'],
                    id=data['user']['id'],
                    avatar_hash=(data['user']['avatar'] if not None else ""),
                    flags=self.data['user']['flags']
                )


    async def __send_data(self, payload):
        payload = json.dumps(payload).encode()

        try:
            await self.ws.send(payload)

        except PayloadTooBig:
            print('Payload too big, couldn\'t send message to server.')


    async def __heartbeat(self):
        while True:
            payload = {
                'op': 1,
                'd': self.session_id
            }

            await self.__send_data(payload)

            print('sent heartbeat')

            await asyncio.sleep(self.__heartbeat_interval)

    

    def run(self):
        self.loop.create_task(self.connect())

        try:
            self.loop.run_forever()

        except KeyboardInterrupt:
            self.loop.stop()

