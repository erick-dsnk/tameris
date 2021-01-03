import asyncio
import sys
import requests
import websockets
import json

from models.member import Member
from models.channel import Channel
from models.permissions import PermissionOverwrite, Permissions
from models.guild import Guild
from models.role import Role
from models.guild_member import GuildMember

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

        self.guilds = []

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
            
            elif self.__data['t'] == 'GUILD_CREATE':
                guild_obj = Guild(
                    id=data['id'],
                    name=data['name'],
                    icon=data['icon'],
                    splash=data['splash'],
                    discovery_splash=data['discovery_splash'],
                    owner_id=data['owner_id'],
                    region=data['region'],
                    afk_channel_id=data['afk_channel_id'],
                    afk_timeout=data['afk_timeout'],
                    verification_level=data['verification_level'],
                    default_message_notifications=data['default_message_notifications'],
                    explicit_content_filter=data['explicit_content_filter'],
                    roles=[
                        Role(
                            id=r['id'],
                            name=r['name'],
                            color=r['color'],
                            position=r['position'],
                            is_mentionable=r['mentionable'],
                            hoist=r['hoist']
                        ) for r in data['roles']
                    ]
                )

                self.guilds.append(guild_obj)

                await self.events.on_guild_create(guild=guild_obj)
                
            elif self.__data['t'] == 'GUILD_UPDATE':
                guild_obj = Guild(
                    id=data['id'],
                    name=data['name'],
                    icon=data['icon'],
                    splash=data['splash'],
                    discovery_splash=data['discovery_splash'],
                    owner_id=data['owner_id'],
                    region=data['region'],
                    afk_channel_id=data['afk_channel_id'],
                    afk_timeout=data['afk_timeout'],
                    verification_level=data['verification_level'],
                    default_message_notifications=data['default_message_notifications'],
                    explicit_content_filter=data['explicit_content_filter'],
                    roles=[
                        Role(
                            id=r['id'],
                            name=r['name'],
                            color=r['color'],
                            position=r['position'],
                            is_mentionable=r['mentionable'],
                            hoist=r['hoist']
                        ) for r in data['roles']
                    ]
                )

                for guild in self.guilds:
                    if guild.id == guild_obj.id:
                        self.guilds[self.guild.index(guild)] = guild_obj
                
                await self.events.on_guild_update(guild=guild_obj)

            elif self.__data['t'] == 'GUILD_DELETE':
                for guild in self.guilds:
                    if guild.id == data['id']:
                        del self.guilds[self.guild.index(guild)]

                self.events.on_guild_delete(guild_id=data['id'])
                        

            elif self.__data['t'] == 'GUILD_BAN_ADD':
                member_obj = Member(
                    name=data['user']['name'],
                    discriminator=data['user']['discriminator'],
                    id=data['user']['id'],
                    avatar_hash=data['user']['avatar'],
                    is_verified=data['user']['verified'],
                    flags=data['user']['flags'],
                    premium_type=data['user']['premium_type']
                )


                await self.events.on_guild_ban_add(
                    guild_id=data['guild_id'],
                    member=member_obj
                )

            elif self.__data['t'] == 'GUILD_BAN_REMOVE':
                member_obj = Member(
                    name=data['user']['name'],
                    discriminator=data['user']['discriminator'],
                    id=data['user']['id'],
                    avatar_hash=data['user']['avatar'],
                    is_verified=data['user']['verified'],
                    flags=data['user']['flags'],
                    premium_type=data['user']['premium_type']
                )

                await self.events.on_guild_ban_remove(
                    guild_id=data['guild_id'],
                    member=member_obj
                )

            elif self.__data['t'] == 'GUILD_MEMBER_ADD':
                guild_member_obj = GuildMember(
                    user=Member(
                        name=data['user']['name'],
                        discriminator=data['user']['discriminator'],
                        id=data['user']['id'],
                        avatar_hash=data['user']['avatar'],
                        is_verified=data['user']['verified'],
                        flags=data['user']['flags'],
                        premium_type=data['user']['premium_type']
                    ),
                    nickname=data['nick'],
                    roles=data['roles'],
                    joined_at=data['joined_at'],
                    is_deaf=data['deaf'],
                    is_muted=data['muted'],
                    guild_id=data['guild_id']
                )

                await self.events.on_guild_member_add(
                    guild_member=guild_member_obj
                )

            elif self.__data['t'] == 'GUILD_MEMBER_REMOVE':
                member_obj = Member(
                    name=data['user']['name'],
                    discriminator=data['user']['discriminator'],
                    id=data['user']['id'],
                    avatar_hash=data['user']['avatar'],
                    is_verified=data['user']['verified'],
                    flags=data['user']['flags'],
                    premium_type=data['user']['premium_type']
                )

                await self.events.on_guild_member_remove(
                    guild_id=data['guild_id'],
                    member=member_obj
                )

            elif self.__data['t'] == 'GUILD_MEMBER_UPDATE':
                guild_member_obj = GuildMember(
                    user=Member(
                        name=data['user']['name'],
                        discriminator=data['user']['discriminator'],
                        id=data['user']['id'],
                        avatar_hash=data['user']['avatar'],
                        is_verified=data['user']['verified'],
                        flags=data['user']['flags'],
                        premium_type=data['user']['premium_type']
                    ),
                    nickname=data['nick'],
                    roles=data['roles'],
                    joined_at=data['joined_at'],
                    is_deaf=data['deaf'] if 'deaf' in data.keys() else False,
                    is_muted=data['muted'] if 'deaf' in data.keys() else False,
                    guild_id=data['guild_id']
                )

                await self.events.on_guild_member_update(
                    guild_member=guild_member_obj
                )

            
            elif self.__data['t'] == 'GUILD_ROLE_CREATE':
                role_obj = Role(
                    id=data['role']['id'],
                    name=data['role']['name'],
                    color=data['role']['color'],
                    position=data['role']['position'],
                    permissions=Permissions(permission_integer=int(data['role']['permissions']))
                )

                await self.events.on_guild_role_create(
                    guild_id=data['guild_id'],
                    role=role_obj
                )


            elif self.__data['t'] == 'GUILD_ROLE_UPDATE':
                role_obj = Role(
                    id=data['role']['id'],
                    name=data['role']['name'],
                    color=data['role']['color'],
                    position=data['role']['position'],
                    permissions=Permissions(permission_integer=int(data['role']['permissions']))
                )

                await self.events.on_guild_role_update(
                    guild_id=data['guild_id'],
                    role=role_obj
                )

            elif self.__data['t'] == 'GUILD_ROLE_DELETE':
                await self.events.on_guild_role_delete(
                    guild_id=data['guild_id'],
                    role_id=data['role_id']
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

    async def send_message(self, message, channel_id):
        resp = await self.__handler.post(
            endpoint=f'/channels/{channel_id}/messages',
            body={
                'content': message
            }
        )

        print(resp)
