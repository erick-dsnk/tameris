class Voice:
    def __init__(
        self,
        channel_id,
        user_id,
        session_id,
        deaf,
        mute,
        self_deaf,
        self_mute,
        self_video,
        suppress
    ):
        self.channel_id = channel_id
        self.user_id = user_id
        self.session_id = session_id
        self.deaf = deaf
        self.mute = mute
        self.self_deaf = self_deaf
        self.self_mute = self_mute
        self.self_video = self_video
        self.suppress = suppress
