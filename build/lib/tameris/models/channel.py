class Channel:
    def __init__(
        self,
        id,
        type,
        guild_id,
        position,
        permission_overwrites,
        name,
        topic,
        is_nsfw,
        slowmode_interval,
        parent_id,
        last_message_id = None,
        **kwargs
    ): 
        self.id = id
        self.type = type
        self.guild_id = guild_id
        self.position = position
        self.permission_overwrites = permission_overwrites
        self.name = name
        self.topic = topic
        self.is_nsfw = is_nsfw
        self.last_message_id = last_message_id
        self.slowmode_interval = slowmode_interval
        self.parent_category_id = parent_id

        if type == 'GUILD_VOICE':
            self.bitrate = kwargs.get('bitrate')
            self.user_limit = kwargs.get('user_limit')

class ChannelSettings:
    def __init__(
        self,
        name = None,
        type = None,
        position = None,
        topic = None,
        nsfw = None,
        rate_limit_per_user = None,
        bitrate = None,
        user_limit = None,
        permission_overwrites = None,
        parent_id = None
    ):
        self.name = name
        self.type = type
        self.position = position
        self.topic = topic
        self.nsfw = nsfw
        self.rate_limit_per_user = rate_limit_per_user
        self.bitrate = bitrate
        self.user_limit = user_limit
        self.permission_overwrites = permission_overwrites
        self.parent_id = parent_id
