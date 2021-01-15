
from typing import List

from tameris.models.member import Member
from tameris.models.channel import Channel, ChannelSettings
from tameris.models.attachment import Attachment
from tameris.models.guild import Guild
from tameris.models.emoji import Emoji
from tameris.models.role import Role
from tameris.models.message import Message
from tameris.models.permissions import *
from tameris.models.embed import *

class Utilities:
    def __init__(self, client):
        self.client = client

    async def get_member(self, member_id: str) -> Member:
        status_code, response = await self.client.__handler.get(endpoint=f'/users/{member_id}')

        if status_code == 200:
            member = Member(
                name=response['username'],
                discriminator=response['discriminator'],
                id=response['id'],
                avatar_hash=response['avatar'],
                is_verified=response['verified'],
                flags=response['flags'],
                premium_type=response['premium_type']
            )

            return member
        
        else:
            return None

    async def get_channel(self, channel_id: str) -> Channel:
        status_code, response = await self.client.__handler.get(endpoint=f'/channels/{channel_id}')

        if status_code == 200:
            channel = Channel(
                id=response['id'],
                type=response['type'],
                guild_id=response['guild_id'],
                position=response['position'],
                permission_overwrites=PermissionOverwrite(
                    id=response['permission_overwrites']['id'],
                    type=response['permission_overwrites']['type'],
                    allow=response['permission_overwrites']['allow'],
                    deny=response['permission_overwrites']['deny']
                ),
                name=response['name'],
                topic=response['topic'],
                is_nsfw=response['nsfw'],
                slowmode_interval=response['slowmode_interval'],
                parent_id=response['parent_id'],
                last_message_id=response['last_message_id'],
                user_limit=response['user_limit'] if response['type'] == 2 else None,
                bitrate=response['bitrate'] if response['type'] == 2 else None
            )

            return channel
        
        else:
            return None

    async def modify_channel(self, channel_id: str, channel_settings: ChannelSettings) -> Channel:
        _channel_settings = {}

        if channel_settings.name:
            _channel_settings['name'] = channel_settings.name
        
        if channel_settings.type:
            _channel_settings['type'] = channel_settings.type

        if channel_settings.topic:
            _channel_settings['topic'] = channel_settings.topic

        if channel_settings.position:
            _channel_settings['position'] = channel_settings.position

        if channel_settings.nsfw:
            _channel_settings['nsfw'] = channel_settings.nsfw

        if channel_settings.rate_limit_per_user:
            _channel_settings['rate_limit_per_user'] = channel_settings.rate_limit_per_user
        
        if channel_settings.bitrate:
            _channel_settings['bitrate'] = channel_settings.bitrate

        if channel_settings.user_limit:
            _channel_settings['user_limit'] = channel_settings.user_limit

        if channel_settings.permission_overwrites:
            _channel_settings['permission_overwrites'] = channel_settings.permission_overwrites

        if channel_settings.parent_id:
            _channel_settings['parent_id'] = channel_settings.parent_id

        status_code, response = await self.client.__handler.patch(
            endpoint=f'/channels/{channel_id}',
            body=_channel_settings
        )

        if status_code == 200:
            channel = Channel(
                id=response['id'],
                type=response['type'],
                guild_id=response['guild_id'],
                position=response['position'],
                permission_overwrites=PermissionOverwrite(
                    id=response['permission_overwrites']['id'],
                    type=response['permission_overwrites']['type'],
                    allow=response['permission_overwrites']['allow'],
                    deny=response['permission_overwrites']['deny']
                ),
                name=response['name'],
                topic=response['topic'],
                is_nsfw=response['nsfw'],
                slowmode_interval=response['slowmode_interval'],
                parent_id=response['parent_id'],
                last_message_id=response['last_message_id'],
                user_limit=response['user_limit'] if response['type'] == 2 else None,
                bitrate=response['bitrate'] if response['type'] == 2 else None
            )

            return channel
        
        else:
            return None


    async def delete_channel(self, channel_id):
        status_code, response = await self.client.__handler.delete(
            endpoint=f'/channels/{channel_id}'
        )

        if status_code == 200:
            return response
        
        else:
            return None

    async def get_message(self, channel_id, message_id) -> Message:
        status_code, response = await self.client.__handler.get(
            endpoint=f'/channels/{channel_id}/messages/{message_id}'
        )

        if status_code == 200:
            message = Message(
                id=response['id'],
                channel_id=response['channel_id'],
                author=Member(
                    name=response['author'],
                    discriminator=response['author']['discriminator'],
                    id=response['author']['id'],
                    avatar_hash=response['author']['avatar'],
                    is_verified=response['author']['verified'],
                    flags=response['author']['flags'],
                    premium_type=response['author']['premium_type']
                ),
                content=response['content'],
                timestamp=response['timestamp'],
                edited_timestamp=response['edited_timestamp'],
                tts=response['tts'],
                mention_everyone=response['mention_everyone'],
                mentions=[
                    Member(
                        name=mn['username'],
                        discriminator=mn['discriminator'],
                        id=mn['id'],
                        avatar_hash=mn['avatar'],
                        is_verified=mn['verified'],
                        flags=mn['flags'],
                        premium_type=mn['premium_type']
                    ) for mn in response['mentions']
                ],
                mention_roles=response['mention_roles'],
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
                    ) for a in response['attachments']
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
                                name=f['name'],
                                value=f['value']
                            ) for f in e['fields']
                        ]
                    ) for e in response['embeds']
                ],
                pinned=response['pinned']
            )

            return message

    
    async def get_messages(self, channel_id, limit = 50, **kwargs) -> List[Message]:
        if limit > 100 or limit < 1:
            return
        
        extra_params = {}

        if 'around' in kwargs.keys():
            if len(kwargs.keys()) < 1:
                extra_params['around'] = kwargs.get('around')

        if 'before' in kwargs.keys():
            if len(kwargs.keys()) < 1:
                extra_params['around'] = kwargs.get('before')

        if 'after' in kwargs.keys():
            if len(kwargs.keys()) < 1:
                extra_params['around'] = kwargs.get('after')

        status_code, response = await self.client.__handler.get(
            endpoint=f'/channels/{channel_id}/messages',
            extra_params=extra_params
        )

        if status_code == 200:
            return [
                Message(
                    id=m['id'],
                    channel_id=m['channel_id'],
                    author=Member(
                        name=m['author'],
                        discriminator=m['author']['discriminator'],
                        id=m['author']['id'],
                        avatar_hash=m['author']['avatar'],
                        is_verified=m['author']['verified'],
                        flags=m['author']['flags'],
                        premium_type=m['author']['premium_type']
                    ),
                    content=m['content'],
                    timestamp=m['timestamp'],
                    edited_timestamp=m['edited_timestamp'],
                    tts=m['tts'],
                    mention_everyone=m['mention_everyone'],
                    mentions=[
                        Member(
                            name=mn['username'],
                            discriminator=mn['discriminator'],
                            id=mn['id'],
                            avatar_hash=mn['avatar'],
                            is_verified=mn['verified'],
                            flags=mn['flags'],
                            premium_type=mn['premium_type']
                        ) for mn in m['mentions']
                    ],
                    mention_roles=m['mention_roles'],
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
                        ) for a in response['attachments']
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
                                    name=f['name'],
                                    value=f['value']
                                ) for f in e['fields']
                            ]
                        ) for e in response['embeds']
                    ],
                    pinned=response['pinned']
                ) for m in response
            ]
        
        else:
            return None

    async def get_guild(self, guild_id: str) -> Guild:
        status_code, response = await self.client.__handler.get(endpoint=f'/guilds/{guild_id}')

        if status_code == 200:
            guild = Guild(
                id=response['id'],
                name=response['name'],
                icon=response['icon'],
                splash=response['splash'],
                discovery_splash=response['discovery_splash'],
                owner_id=response['owner_id'],
                region=response['region'],
                afk_channel_id=response['afk_channel_id'],
                afk_timeout=response['afk_timeout'],
                verification_level=response['verification_level'],
                default_message_notifications=response['default_message_notifications'],
                explicit_content_filter=response['explicit_content_filter'],
                roles=[
                    Role(
                        id=r['id'],
                        name=r['name'],
                        color=r['color'],
                        position=r['position'],
                        permissions=Permissions(int(r['permissions'])),
                        is_mentionable=r['mentionable'],
                        hoist=r['hoist']
                    ) for r in response['roles']
                ],
                emojis=[
                    Emoji(
                        id=e['id'],
                        name=e['name'],
                        is_animated=e['animated'] if 'animated' in e.keys() else False
                    ) for e in response['emojis']
                ],
                features=response['features'],
                mfa_level=response['mfa_level'],
                system_channel_id=response['system_channel_id'],
                system_channel_flags=response['system_channel_flags'],
                rules_channel_id=response['rules_channel_id'],
                vanity_url_code=response['vanity_url_code'],
                description=response['description'],
                banner=response['banner'],
                premium_tier=response['premium_tier'],
                preferred_locale=response['preferred_locale'],
                public_updates_channel_id=response['public_updates_channel_id']
            )

            return guild

        else:
            return None