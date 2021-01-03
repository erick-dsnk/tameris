class Role:
    def __init__(
        self,
        id,
        name,
        color,
        position,
        permissions,
        is_mentionable,
        hoist
    ):
        self.id = id
        self.name = name
        self.color = color
        self.position = position
        self.permissions = permissions
        self.is_mentionable = is_mentionable
        self.hoist = hoist