class Webhook:
    def __init__(
        self,
        id,
        type,
        channel_id,
        name,
        avatar,
        application_id
    ):
        self.id = id
        self.type = type
        self.channel_id = channel_id
        self.name = name
        self.avatar = avatar
        self.application_id = application_id