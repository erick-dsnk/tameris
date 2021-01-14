
from tameris.models.member import Member
from tameris.models.channel import Channel
from tameris.models.guild import Guild
from tameris.models.emoji import Emoji
from tameris.models.role import Role
from tameris.models.permissions import *

class Utilities:
    def __init__(self, client):
        self.client = client

    async def get_member(self, member_id: str) -> Member:
        response = await self.client.__handler.get(endpoint=f'/users/{member_id}')

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

    async def get_channel(self, channel_id: str) -> Channel:
        response = await self.client.__handler.get(endpoint=f'/channels/{channel_id}')

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

    async def get_guild(self, guild_id: str) -> Guild:
        response = await self.client.__handler.get(endpoint=f'/guilds/{guild_id}')

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