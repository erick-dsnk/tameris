# Tameris - Python Discord API wrapper!
Tameris is focused on customizability in your Discord bots as well as flexibility and expandability!

## Examples

Creating a simple bot with Tameris

```py
bot = Client(bot_token='token', command_prefix='+')

class HelloCommand(Command):
    async def run(self, context: Context, call_arguments):
        await bot.send_message(content=f'Hello! @{context.author.name}#{context.author.discriminator}', channel_id=context.channel.id)


async def ready():
    print('Logged in.')

async def on_message(message):
    await bot.process_commands(message)

bot.events.on_ready = ready
bot.events.on_message_create = on_message

bot.register_command(HelloCommand, 'hello')

bot.run()
```