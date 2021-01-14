class Message:
    def __init__(
        self,
        id,
        channel_id,
        author,
        content,
        timestamp,
        edited_timestamp,
        tts,
        mention_everyone,
        mentions,
        mention_roles,
        attachments,
        embeds,
        pinned,
        type
    ):
        self.id = id
        self.channel_id = channel_id
        self.author = author
        self.content = content
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.tts = tts
        self.mention_everyone = mention_everyone
        self.mentions = mentions
        self.mention_roles = mention_roles
        self.attachments = attachments
        self.embeds = embeds
        self.pinned = pinned
        self.type = type
