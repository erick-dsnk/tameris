from client import Client

from models.member import Member

class Utilities:
    def __init__(self, client: Client):
        self.client = client

    async def get_member(self, member_id: str) -> Member:
        response = self.client.__handler.get(endpoint=f'/users/{member_id}')

        member = Member(
            name=response['username'],
            discriminator=response['discriminator'],
            id=response['id'],
            avatar_hash=response['avatar'],
            is_verified=response['verified'],
            flags=response['flags'],
            premium_type=response['premium_type']
        )

        return member