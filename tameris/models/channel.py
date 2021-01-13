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