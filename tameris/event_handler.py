from typing import Callable

class EventHandler:
    def __init__(
        self,
        on_ready: Callable = None,

        on_guild_create: Callable = None,
        on_guild_delete: Callable = None,
        on_guild_update: Callable = None,
        on_guild_ban_add: Callable = None,
        on_guild_ban_remove: Callable = None,
        on_guild_member_add: Callable = None,
        on_guild_member_remove: Callable = None,
        on_guild_member_update: Callable = None,
        on_guild_role_create: Callable = None,
        on_guild_role_update: Callable = None,
        on_guild_role_delete: Callable = None,

        on_channel_create: Callable = None,
        on_channel_update: Callable = None,
        on_channel_delete: Callable = None,

        on_message_create: Callable = None,
        on_message_update: Callable = None,
        on_message_delete: Callable = None,
        on_message_delete_bulk: Callable = None,
        on_message_reaction_add: Callable = None,
        on_message_reaction_remove: Callable = None,
        on_message_reaction_remove_all: Callable = None
    ):
        self.on_ready = on_ready if on_ready is not None else self._on_ready

        self.on_guild_create = on_guild_create if on_guild_create is not None else self._on_guild_create
        self.on_guild_delete = on_guild_delete if on_guild_delete is not None else self._on_guild_delete
        self.on_guild_update = on_guild_update if on_guild_update is not None else self._on_guild_update
        self.on_guild_ban_add = on_guild_ban_add if on_guild_ban_add is not None else self._on_guild_ban_add
        self.on_guild_ban_remove = on_guild_ban_remove if on_guild_ban_remove is not None else self._on_guild_ban_remove
        self.on_guild_member_add = on_guild_member_add if on_guild_member_add is not None else self._on_guild_member_add
        self.on_guild_member_remove = on_guild_member_remove if on_guild_member_remove is not None else self._on_guild_member_remove
        self.on_guild_member_update = on_guild_member_update if on_guild_member_update is not None else self._on_guild_member_update
        self.on_guild_role_create = on_guild_role_create if on_guild_role_create is not None else self._on_guild_role_create
        self.on_guild_role_update = on_guild_role_update if on_guild_role_update is not None else self._on_guild_role_update
        self.on_guild_role_delete = on_guild_role_delete if on_guild_role_delete is not None else self._on_guild_role_delete
        
        self.on_channel_create = on_channel_create if on_channel_create is not None else self._on_channel_create
        self.on_channel_update = on_channel_update if on_channel_update is not None else self._on_channel_update
        self.on_channel_delete = on_channel_delete if on_channel_delete is not None else self._on_channel_delete

        self.on_message_create = on_message_create if on_message_create is not None else self._on_message_create
        self.on_message_update = on_message_update if on_message_update is not None else self._on_message_update
        self.on_message_delete = on_message_delete if on_message_delete is not None else self._on_message_delete
        self.on_message_delete_bulk = on_message_delete_bulk if on_message_delete_bulk is not None else self._on_message_delete_bulk
        self.on_message_reaction_add = on_message_reaction_add if on_message_reaction_add is not None else self._on_message_reaction_add
        self.on_message_reaction_remove = on_message_reaction_remove if on_message_reaction_remove is not None else self._on_message_reaction_remove
        self.on_message_reaction_remove_all = on_message_reaction_remove_all if on_message_reaction_remove_all is not None else self._on_message_reaction_remove_all


    async def _on_ready(self):
        print('Logged in.')

    async def _on_guild_create(self, guild):
        pass

    async def _on_guild_delete(self, guild_id):
        pass

    async def _on_guild_update(self, guild):
        pass

    async def _on_guild_ban_add(self, guild_id, member):
        pass

    async def _on_guild_ban_remove(self, guild_id, member):
        pass

    async def _on_guild_member_add(self, guild_member):
        pass

    async def _on_guild_member_update(self, guild_member):
        pass

    async def _on_guild_member_remove(self, guild_id, member):
        pass

    async def _on_guild_role_create(self, guild_id, role):
        pass

    async def _on_guild_role_update(self, guild_id, role):
        pass

    async def _on_guild_role_delete(self, guild_id, role_id):
        pass

    async def _on_channel_create(self, channel):
        pass

    async def _on_channel_update(self, channel):
        pass

    async def _on_channel_delete(self, channel):
        pass

    async def _on_message_create(self, message):
        pass

    async def _on_message_update(self, message):
        pass

    async def _on_message_delete(self, message_id, channel_id, guild_id):
        pass

    async def _on_message_delete_bulk(self, message_ids, channel_id, guild_id):
        pass

    async def _on_message_reaction_add(self, reaction, member, message_id, channel_id):
        pass

    async def _on_message_reaction_remove(self, reaction, member_id, message_id, channel_id, guild_id):
        pass

    async def _on_message_reaction_remove_all(self, message_id, channel_id, guild_id):
        pass