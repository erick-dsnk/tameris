import asyncio

import sys
from typing import List
import requests
import websockets
import json

from tameris.models.member import Member
from tameris.models.channel import Channel
from tameris.models.permissions import PermissionOverwrite, Permissions
from tameris.models.guild import Guild
from tameris.models.role import Role
from tameris.models.guild_member import GuildMember
from tameris.models.message import Message
from tameris.models.attachment import Attachment
from tameris.models.emoji import Emoji
from tameris.models.embed import *

from tameris.commands.command import Command
from tameris.commands.context import Context

from tameris.core.extensions import Utilities

from tameris.core.request_handler import RequestHandler
from tameris.core.event_handler import EventHandler

from websockets.exceptions import PayloadTooBig

class ClientPresence:
    def __init__(
        self,
        name: str,
        type: str,
        status: str,
        **kwargs
    ):
        self.name = name
        self.type = type
        self.status = status

        if self.type == 'game':
            self.type = 0
        elif self.type == 'streaming':
            self.type = 1
        elif self.type == 'listening':
            self.type = 2
        elif self.type == 'custom':
            self.type = 4
        elif self.type == 'competing':
            self.type = 5

        if kwargs.get('url'):
            self.url = kwargs.get('url')



class Client:
    def __init__(self, bot_token: str, command_prefix: str):
        self.token = bot_token
        self.command_prefix = command_prefix

        self.commands: List[Command] = []

        self.__handler = RequestHandler(token=self.token)
        self.events = EventHandler()
        self.utils = Utilities(self)

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
            self.__data = json.loads(await self.ws.recv())

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
                            permissions=Permissions(int(r['permission_integer'])),
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
                            permissions=Permissions(int(r['permission_integer'])),
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
                    name=data['user']['username'],
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
                    name=data['user']['username'],
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
                        name=data['user']['username'],
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
                    name=data['user']['username'],
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
                        name=data['user']['username'],
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
                    is_muted=data['muted'] if 'muted' in data.keys() else False,
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

            
            elif self.__data['t'] == 'MESSAGE_CREATE':
                message_obj = Message(
                    id=data['id'],
                    channel_id=data['channel_id'],
                    author=Member(
                        name=data['author']['username'],
                        discriminator=data['author']['discriminator'],
                        id=data['author']['id'],
                        avatar_hash=data['author']['avatar'],
                        is_verified=data['author']['verified'],
                        flags=data['author']['flags'],
                        premium_type=data['author']['premium_type']
                    ),
                    content=data['content'],
                    timestamp=data['timestamp'],
                    edited_timestamp=data['edited_timestamp'],
                    tts=data['tts'],
                    mention_everyone=data['mention_everyone'],
                    mentions=[
                        Member(
                            name=m['username'],
                            discriminator=data['discriminator'],
                            id=m['id'],
                            avatar_hash=m['avatar'],
                            is_verified=m['verified'],
                            flags=m['flags'],
                            premium_type=m['premium_type']
                        ) for m in data['mentions']
                    ],
                    mention_roles=data['mention_roles'],
                    attachments=[
                        (
                            Attachment(
                                id=a['id'],
                                filename=a['filename'],
                                size=a['size'],
                                url=a['url'],
                                proxy_url=a['proxy_url'],
                                height=a['height'],
                                width=a['width']
                            ) if ('height' in a.keys() and 'width' in a.keys()) else Attachment(
                                id=a['id'],
                                filename=a['filename'],
                                size=a['size'],
                                url=a['url'],
                                proxy_url=a['proxy_url']
                            )
                        ) for a in a['attachments']
                    ],
                    embeds=[
                        Embed(
                            title=e['title'],
                            description=e['description'],
                            url=e['url'],
                            timestamp=e['timestamp'],
                            color=e['color'],
                            footer=EmbedFooter(
                                text=e['footer']['text'],
                                icon_url=e['footer']['icon_url'],
                                proxy_icon_url=e['footer']['proxy_icon_url']
                            ),
                            image=EmbedImage(
                                url=e['image']['url'],
                                proxy_url=e['image']['proxy_url'],
                                height=e['image']['height'],
                                width=e['image']['width']
                            ),
                            thumbnail=EmbedThumbnail(
                                url=e['thumbnail']['url'],
                                proxy_url=e['thumbnail']['proxy_url'],
                                height=e['thumbnail']['height'],
                                width=e['thumbnail']['width']
                            ),
                            video=EmbedVideo(
                                url=e['video']['url'],
                                height=e['video']['height'],
                                width=e['video']['width']
                            ),
                            provider=EmbedProvider(
                                name=e['provider']['name'],
                                url=e['provider']['url']
                            ),
                            author=EmbedAuthor(
                                name=e['author']['name'],
                                url=e['author']['url'],
                                icon_url=e['author']['icon_url'],
                                proxy_icon_url=e['author']['proxy_icon_url']
                            ),
                            fields=[
                                EmbedField(
                                    name=e['name'],
                                    value=e['value']
                                ) for f in e['fields']
                            ]
                        ) for e in data['embeds']
                    ],
                    pinned=data['pinned']
                )
                
                await self.events.on_message_create(
                    message=message_obj
                )

            elif self.__data['t'] == 'MESSAGE_UPDATE':
                message_obj = Message(
                    id=data['id'],
                    channel_id=data['channel_id'],
                    author=Member(
                        name=data['author']['username'],
                        discriminator=data['author']['discriminator'],
                        id=data['author']['id'],
                        avatar_hash=data['author']['avatar'],
                        is_verified=data['author']['verified'],
                        flags=data['author']['flags'],
                        premium_type=data['author']['premium_type']
                    ),
                    content=data['content'],
                    timestamp=data['timestamp'],
                    edited_timestamp=data['edited_timestamp'],
                    tts=data['tts'],
                    mention_everyone=data['mention_everyone'],
                    mentions=[
                        Member(
                            name=m['username'],
                            discriminator=data['discriminator'],
                            id=m['id'],
                            avatar_hash=m['avatar'],
                            is_verified=m['verified'],
                            flags=m['flags'],
                            premium_type=m['premium_type']
                        ) for m in data['mentions']
                    ],
                    mention_roles=data['mention_roles'],
                    attachments=[
                        (
                            Attachment(
                                id=a['id'],
                                filename=a['filename'],
                                size=a['size'],
                                url=a['url'],
                                proxy_url=a['proxy_url'],
                                height=a['height'],
                                width=a['width']
                            ) if ('height' in a.keys() and 'width' in a.keys()) else Attachment(
                                id=a['id'],
                                filename=a['filename'],
                                size=a['size'],
                                url=a['url'],
                                proxy_url=a['proxy_url']
                            )
                        ) for a in a['attachments']
                    ],
                    embeds=[
                        Embed(
                            title=e['title'],
                            description=e['description'],
                            url=e['url'],
                            timestamp=e['timestamp'],
                            color=e['color'],
                            footer=EmbedFooter(
                                text=e['footer']['text'],
                                icon_url=e['footer']['icon_url'],
                                proxy_icon_url=e['footer']['proxy_icon_url']
                            ),
                            image=EmbedImage(
                                url=e['image']['url'],
                                proxy_url=e['image']['proxy_url'],
                                height=e['image']['height'],
                                width=e['image']['width']
                            ),
                            thumbnail=EmbedThumbnail(
                                url=e['thumbnail']['url'],
                                proxy_url=e['thumbnail']['proxy_url'],
                                height=e['thumbnail']['height'],
                                width=e['thumbnail']['width']
                            ),
                            video=EmbedVideo(
                                url=e['video']['url'],
                                height=e['video']['height'],
                                width=e['video']['width']
                            ),
                            provider=EmbedProvider(
                                name=e['provider']['name'],
                                url=e['provider']['url']
                            ),
                            author=EmbedAuthor(
                                name=e['author']['name'],
                                url=e['author']['url'],
                                icon_url=e['author']['icon_url'],
                                proxy_icon_url=e['author']['proxy_icon_url']
                            ),
                            fields=[
                                EmbedField(
                                    name=e['name'],
                                    value=e['value']
                                ) for f in e['fields']
                            ]
                        ) for e in data['embeds']
                    ],
                    pinned=data['pinned']
                )
                
                await self.events.on_message_update(
                    message=message_obj
                )

            elif self.__data['t'] == 'MESSAGE_DELETE':
                message_id = data['id']
                channel_id = data['channel_id']
                guild_id = data['guild_id']

                await self.events.on_message_delete(
                    message_id=message_id,
                    channel_id=channel_id,
                    guild_id=guild_id
                )

            elif self.__data['t'] == 'MESSAGE_DELETE_BULK':
                message_ids = data['message_ids']
                channel_id = data['channel_id']
                guild_id = data['guild_id']

                await self.events.on_message_delete_bulk(
                    message_ids=message_ids,
                    channel_id=channel_id,
                    guild_id=guild_id
                )

            elif self.__data['t'] == 'MESSAGE_REACTION_ADD':
                channel_id = data['channel_id']
                message_id = data['message_id']
                guild_id = data['guild_id']
                member = GuildMember(
                    user=Member(
                        name=data['member']['user']['username'],
                        discriminator=data['member']['user']['discriminator'],
                        id=data['member']['user']['id'],
                        avatar_hash=data['member']['user']['avatar'],
                        is_verified=data['member']['user']['verified'],
                        flags=data['member']['user']['flags'],
                        premium_type=data['member']['user']['premium_type']
                    ),
                    nickname=data['member']['nickname'],
                    roles=data['member']['roles'],
                    joined_at=data['member']['joined_at'],
                    is_deaf=data['deaf'],
                    is_muted=data['muted'],
                    guild_id=guild_id
                )
                emoji = Emoji(
                    id=data['emoji']['id'],
                    name=data['emoji']['name'],
                    is_animated=data['emoji']['animated'] if 'animated' in data['emoji'].keys() else False
                )

                await self.events.on_message_reaction_add(
                    reaction=emoji,
                    member=member,
                    message_id=message_id,
                    channel_id=channel_id
                )

            elif self.__data['t'] == 'MESSAGE_REACTION_REMOVE':
                emoji = Emoji(
                    id=data['emoji']['id'],
                    name=data['emoji']['name'],
                    is_animated=data['emoji']['animated'] if 'animated' in data['emoji'].keys() else False
                )
                member_id = data['user_id']
                channel_id = data['channel_id']
                guild_id = data['guild_id']
                message_id = data['message_id']

                await self.events.on_message_reaction_remove(
                    reaction=emoji,
                    member_id=member_id,
                    message_id=message_id,
                    channel_id=channel_id,
                    guild_id=guild_id
                )

            elif self.__data['t'] == 'MESSAGE_REACTION_REMOVE_ALL':
                channel_id = data['channel_id']
                message_id = data['message_id']
                guild_id = data['guild_id']

                await self.events.on_message_reaction_remove_all(
                    message_id=message_id,
                    channel_id=channel_id,
                    guild_id=guild_id
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


    def register_command(self, command: Command, name: str):
        self.commands.append(command(self, name))


    async def process_commands(self, message: Message):
        for command in self.commands:
            if command.was_invoked(message.content):
                args = message.content.split(' ')

                del args[0]

                author = message.author
                channel = self.utils.get_channel(channel_id=message.channel_id)
                guild = self.utils.get_guild(guild_id=channel.guild_id)

                context = Context(author=author, message=message, channel=channel, guild=guild)
                
                await command.run(context, args)


    async def send_message(self, message, channel_id):
        resp = await self.__handler.post(
            endpoint=f'/channels/{channel_id}/messages',
            body={
                'content': message
            }
        )

        print(resp)


    async def update_presence(self, presence: ClientPresence):
        if presence.url:
            payload = {
                'op': 3,
                'd': {
                    'activities': [
                        {
                            'name': presence.name,
                            'type': presence.type,
                            'url': presence.url
                        }
                    ],
                    'status': presence.status,
                    'afk': False
                }
            }
        
        else:
            payload = {
                'op': 3,
                'd': {
                    'activities': [
                        {
                            'name': presence.name,
                            'type': presence.type
                        }
                    ],
                    'status': presence.status,
                    'afk': False
                }
            }

        await self.__send_data(payload)