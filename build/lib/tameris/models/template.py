class Template:
    def __init__(
        self,
        code,
        name,
        description,
        usage_count,
        creator_id,
        creator,
        created_at,
        updated_at,
        source_guild_id,
        serialized_source_guild,
        is_dirty
    ):
        self.code = code
        self.name = name
        self.description = description
        self.usage_count = usage_count
        self.creator_id = creator_id
        self.creator = creator
        self.created_at = created_at
        self.updated_at = updated_at
        self.source_guild_id = source_guild_id
        self.serialized_source_guild = serialized_source_guild
        self.is_dirty = is_dirty

