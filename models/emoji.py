

class Emoji:
    def __init__(
        self,
        id,
        name,
        creator,
        requires_colons,
        is_animated
    ):
        self.id = id
        self.name = name
        self.creator = creator
        self.requires_colons = requires_colons
        self.is_animated = is_animated