

class GuildMember:
    def __init__(
        self,
        user,
        nickname,
        roles,
        joined_at,
        is_deaf,
        is_muted,
        **kwargs
    ):
        self.user = user
        self.nickname = nickname
        self.roles = roles
        self.joined_at = joined_at
        self.is_deaf = is_deaf
        self.is_muted = is_muted

        if kwargs.get('guild_id'): self.guild_id = kwargs.get('guild_id')
        else: self.guild_id = None