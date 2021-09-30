import json

import discord
from discord.ext import commands
import asyncio


class RemoveRR(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ReactionRR ready.")

    try:
        with open("Files/reaction_roles.json") as file:
            reaction_roles_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        with open("Files/reaction_roles.json", "w") as file:
            json.dump({}, file)
    @commands.has_permissions(administrator=True)
    @commands.command(name="removeall")
    async def remove_all(self,ctx):
        guild_id = ctx.guild.id
        jsondata = RemoveRR.reaction_roles_data[f'{guild_id}']
        for item in jsondata:
            channel_id = item["channelID"]
            message_id = item["messageID"]
            channel = await self.client.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)
            users = set()
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.id != self.client.user.id:
                        await reaction.remove(user)
                        await asyncio.sleep(0.5)
        member = await self.client.fetch_user(ctx.author.id)
        await ctx.message.delete()
        await member.send(f'Alle Reaktionen in **{ctx.guild.name}** wurden entfernt!', file=discord.File('Files/Bonobo.jpg'))


def setup(client):
    client.add_cog(RemoveRR(client))