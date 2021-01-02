from client import Client

with open('test_bot_token.txt', 'r') as f:
    token = f.read()

bot = Client(bot_token=token)

bot.run()