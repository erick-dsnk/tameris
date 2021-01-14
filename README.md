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