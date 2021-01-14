from tameris.models.member import Member
from tameris.models.channel import Channel
from tameris.models.guild import Guild
from tameris.models.message import Message

class Context:
    def __init__(
        self,
        author: Member,
        message: Message,
        channel: Channel,
        guild: Guild
    ):
        self.author = author
        self.message = message
        self.channel = channel
        self.guild = guild