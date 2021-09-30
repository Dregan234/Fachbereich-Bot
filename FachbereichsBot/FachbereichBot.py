import discord
from discord.ext import commands
import utils.json_loader

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


@client.event
async def on_ready():
    print(f'BotId: {client.user.id} - Name: {client.user.name}')

if __name__ == '__main__':
    for extensions in initial_extensions:
        client.load_extension(extensions)

client.run(Fachbereich)