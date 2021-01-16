# Tameris - Python Discord API wrapper!
Tameris is focused on customizability in your Discord bots as well as flexibility and expandability!

## Examples

1. Creating a bot with Tameris
```py
from tameris.core.client import Client

bot = Client(bot_token='my bot token', command_prefix='+')

async def on_ready():
    print('bot is ready')

bot.events.on_ready = on_ready

bot.run()
```

2. Making a command
```py
from tameris.core.client import Client
from tameris.commands.command import Command
from tameris.commands.context import Context

bot = Client(bot_token='my bot token', command_prefix='+')

class HelloCommand(Command):
    async def run(self, context: Context, call_arguments):
        await bot.send_message(message=f'Hello! @{context.author.name}#{context.author.discriminator}', channel_id=context.channel.id)
```