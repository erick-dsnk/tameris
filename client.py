import asyncio
import sys
import requests
import websockets
import json

from models.member import Member
from models.channel import Channel
from models.permissions import PermissionOverwrite

from request_handler import RequestHandler
from event_handler import EventHandler

from websockets.exceptions import PayloadTooBig

class Client:
    def __init__(self, bot_token: str):
        self.token = bot_token

        self.__handler = RequestHandler(token=self.token)
        self.events = EventHandler()

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

        self.__heartbeat_interval = 42.15

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

        await self.events.on_ready()

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
                    name=data['user']['username'],
                    discriminator=data['user']['discriminator'],
                    id=data['user']['id'],
                    avatar_hash=(data['user']['avatar'] if not None else ""),
                    flags=data['user']['flags'],
                    is_verified=data['user']['verified']
                )

            elif self.__data['t'] == 'CHANNEL_CREATE':
                channel_obj = Channel(
                    id=data['id'],
                    type=data['type'],
                    guild_id=data['guild_id'],
                    position=data['position'],
                    permission_overwrites=PermissionOverwrite(
                        id=data['permission_overwrites']['id'],
                        type=data['permission_overwrites']['type'],
                        allow=data['permission_overwrites']['allow'],
                        deny=data['permission_overwrites']['deny']
                    ),
                    name=data['name'],
                    topic=data['topic'],
                    is_nsfw=data['nsfw'],
                    slowmode_interval=data['rate_limit_per_user'],
                    parent_id=data['parent_id'],
                    last_message_id=data['last_message_id'],
                    bitrate=data['bitrate'],
                    user_limit=data['user_limit']
                )

                self.events.on_channel_create(channel=channel_obj)

            elif self.__data['t'] == 'CHANNEL_UPDATE':
                channel_obj = Channel(
                    id=data['id'],
                    type=data['type'],
                    guild_id=data['guild_id'],
                    position=data['position'],
                    permission_overwrites=PermissionOverwrite(
                        id=data['permission_overwrites']['id'],
                        type=data['permission_overwrites']['type'],
                        allow=data['permission_overwrites']['allow'],
                        deny=data['permission_overwrites']['deny']
                    ),
                    name=data['name'],
                    topic=data['topic'],
                    is_nsfw=data['nsfw'],
                    slowmode_interval=data['rate_limit_per_user'],
                    parent_id=data['parent_id'],
                    last_message_id=data['last_message_id'],
                    bitrate=data['bitrate'],
                    user_limit=data['user_limit']
                )

                self.events.on_channel_update(channel=channel_obj)

            elif self.__data['t'] == 'CHANNEL_DELETE':
                channel_obj = Channel(
                    id=data['id'],
                    type=data['type'],
                    guild_id=data['guild_id'],
                    position=data['position'],
                    permission_overwrites=PermissionOverwrite(
                        id=data['permission_overwrites']['id'],
                        type=data['permission_overwrites']['type'],
                        allow=data['permission_overwrites']['allow'],
                        deny=data['permission_overwrites']['deny']
                    ),
                    name=data['name'],
                    topic=data['topic'],
                    is_nsfw=data['nsfw'],
                    slowmode_interval=data['rate_limit_per_user'],
                    parent_id=data['parent_id'],
                    last_message_id=data['last_message_id'],
                    bitrate=data['bitrate'],
                    user_limit=data['user_limit']
                )

                self.events.on_channel_update(channel=channel_obj)

            



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

    async def send_message(self, message, channel_id):
        resp = await self.__handler.post(
            endpoint=f'/channels/{channel_id}/messages',
            body={
                'content': message
            }
        )

        print(resp)