import discord
from discord.ext import commands
import utils.json_loader
import os
import asyncio

BOT_PREFIX = ('!')

client = commands.Bot(intents = discord.Intents.all(), command_prefix='!', status=discord.Status.dnd, activity=discord.Game('Elektrotechnik'))
client.remove_command("help")

initial_extensions = ['cogs.help',
                      'cogs.reactions',
                      'cogs.embedds',
                      'cogs.removerr',
                      'cogs.errorHandler'
                      ]

secret_file = utils.json_loader.read_json("secrets")
Fachbereich = secret_file["Fachbereich"]

async def load_extensions():
    for filename in os.listdir("D:\GitHub\Repos\Fachbereich-Bot\FachbereichsBot\cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(Fachbereich)

@client.event
async def on_ready():
    print(f'BotId: {client.user.id} - Name: {client.user.name}')


if __name__ == '__main__':
    asyncio.run(main()) 