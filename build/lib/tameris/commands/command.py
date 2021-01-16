
class Command:
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
            

    def was_invoked(self, content: str):
        if content.startswith(f'{self.bot.command_prefix}{self.name}'):
            return True
        else:
            return False

    def check(self, context):
        return True

    async def failed_check(self):
        print('User not allowed to use this command.')

    async def run(self, context, call_arguments):
        await self.bot.send_message(f'{self.name} command works\ncommand arguments are: {call_arguments.join(" ")}', context.channel.id)