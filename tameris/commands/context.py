from models.member import Member
from models.channel import Channel
from models.guild import Guild
from models.message import Message

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