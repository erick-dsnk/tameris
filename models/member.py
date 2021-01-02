class Member:
    def __init__(
        self,
        name: str,
        discriminator: str,
        id: int,
        avatar_hash: str,
        is_verified: bool,
        flags: int,
        premium_type: int = None
    ):
        self.name = name
        self.discriminator = discriminator
        self.id = id
        self.avatar_hash = avatar_hash
        self.is_verified = is_verified
        self.flags = flags
        self.premium_type = premium_type