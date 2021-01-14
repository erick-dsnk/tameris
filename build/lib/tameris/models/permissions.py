class Permissions:
    def __init__(
        self,
        permission_integer
    ):
        self.__permission_integer = permission_integer

        self.create_instant_invite = (self.__permission_integer & 0x1) == 0x1
        self.kick_members = (self.__permission_integer & 0x2) == 0x2
        self.ban_members = (self.__permission_integer & 0x4) == 0x4
        self.administrator = (self.__permission_integer & 0x8) == 0x8
        self.manage_channels = (self.__permission_integer & 0x10) == 0x10
        self.manage_guilds = (self.__permission_integer & 0x20) == 0x20
        self.add_reactions = (self.__permission_integer & 0x40) == 0x40
        self.view_audit_log = (self.__permission_integer & 0x80) == 0x80
        self.priority_speaker = (self.__permission_integer & 0x100) == 0x100
        self.stream = (self.__permission_integer & 0x200) == 0x200
        self.view_channel = (self.__permission_integer & 0x400) == 0x400
        self.send_messages = (self.__permission_integer & 0x800) == 0x800
        self.send_tts_messages = (self.__permission_integer & 0x1000) == 0x1000
        self.manage_messages = (self.__permission_integer & 0x2000) == 0x2000
        self.embed_links = (self.__permission_integer & 0x4000) == 0x4000
        self.attach_files = (self.__permission_integer & 0x8000) == 0x8000
        self.read_message_history = (self.__permission_integer & 0x10000) == 0x10000
        self.mention_everyone = (self.__permission_integer & 0x20000) == 0x20000
        self.use_external_emojis = (self.__permission_integer & 0x40000) == 0x40000
        self.view_guild_insights = (self.__permission_integer & 0x80000) == 0x80000
        self.connect = (self.__permission_integer & 0x100000) == 0x100000
        self.speak = (self.__permission_integer & 0x200000) == 0x200000
        self.mute_members = (self.__permission_integer & 0x400000) == 0x400000
        self.deafen_members = (self.__permission_integer & 0x800000) == 0x800000
        self.move_members = (self.__permission_integer & 0x1000000) == 0x1000000
        self.use_vad = (self.__permission_integer & 0x2000000) == 0x2000000
        self.change_nickname = (self.__permission_integer & 0x4000000) == 0x4000000
        self.manage_nicknames = (self.__permission_integer & 0x8000000) == 0x8000000
        self.manage_roles = (self.__permission_integer & 0x10000000) == 0x10000000
        self.manage_webhooks = (self.__permission_integer & 0x20000000) == 0x20000000
        self.manage_emojis = (self.__permission_integer & 0x40000000) == 0x40000000


class PermissionOverwrite:
    def __init__(
        self,
        id,
        type,
        allow,
        deny
    ):
        if type == 0:
            self.type = 'role'

        else:
            self.type = 'user'

        self.id = id
        self.allow = allow
        self.deny = deny