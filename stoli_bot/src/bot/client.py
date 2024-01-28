# client.py
import os
import logging
from interactions import Client, Intents, listen



bot: Client = Client(
    token=os.getenv('DISCORD_TOKEN'),
    intents=Intents.ALL,
    sync_interactions=True,
    asyncio_debug=True,
    logger=logging.getLogger('stolibot'),
    send_command_tracebacks=True,
)

@listen()
async def on_ready() -> None:
    print(f'Logged in as {bot.user}\n'
          f'Guilds:')

    for guild in bot.guilds:
        print(f'\t{guild.name}(id: {guild.id})')

    print(bot.env)


