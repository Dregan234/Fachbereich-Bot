import discord
from discord.ext import commands
import json
import atexit
import uuid
from discord import utils



reaction_roles_data = {}

try:
    with open("Files/reaction_roles.json") as file:
        reaction_roles_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as ex:
    with open("Files/reaction_roles.json", "w") as file:
        json.dump({}, file)


@atexit.register
def store_reaction_roles():
    with open("Files/reaction_roles.json", "w") as file:
        json.dump(reaction_roles_data, file)


class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ReactionRoles ready.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None:
            await user.add_roles(role, reason="ReactionRole")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None:
            await user.remove_roles(role, reason="ReactionRole")

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction(
        self,
        ctx,
        emote,
        role: discord.Role,
        channel: discord.TextChannel,
        title,
        message,
    ):
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        await ctx.message.delete()
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="ra")
    async def reaction_add(
        self, ctx, emote, role: discord.Role, channel: discord.TextChannel, message_id
    ):
        ch = await self.client.fetch_channel(channel.id)
        msg = await ch.fetch_message(message_id)
        await msg.add_reaction(emote)
        await ctx.message.delete()
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reactions(self, ctx):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title="Reaction Roles")
        if data is None:
            embed.description = "Aktuell sind keine Reaction-Roles vorhanden."
        else:
            for index, rr in enumerate(data):
                emote = rr.get("emote")
                role_id = rr.get("roleID")
                role = ctx.guild.get_role(role_id)
                channel_id = rr.get("channelID")
                message_id = rr.get("messageID")
                embed.add_field(
                    name=index,
                    value=f"{emote} - @{role} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                    inline=False,
                )
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="rr")
    async def reaction_remove(self, ctx, index: int):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title=f"Lösche Reaction-Role {index}")
        rr = None
        if data is None:
            embed.description = "Diese Reaction Role wurde nicht gefunden."
        else:
            embed.description = (
                "Willst du diese Reaction-Role wirklich löschen? Drücke dafür auf 🗑️."
            )
            rr = data[index]
            emote = rr.get("emote")
            role_id = rr.get("roleID")
            role = ctx.guild.get_role(role_id)
            channel_id = rr.get("channelID")
            message_id = rr.get("messageID")
            _id = rr.get("id")
            embed.set_footer(text=_id)
            embed.add_field(
                name=index,
                value=f"{emote} - @{role} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                inline=False,
            )
        msg = await ctx.send(embed=embed)
        if rr is not None:
            await msg.add_reaction("🗑️")

            def check(reaction, user):
                return (
                    reaction.message.id == msg.id
                    and user == ctx.message.author
                    and str(reaction.emoji) == "🗑️"
                )

            reaction, user = await self.client.wait_for("reaction_add", check=check)
            data.remove(rr)
            reaction_roles_data[str(guild_id)] = data
            store_reaction_roles()
        await ctx.message.delete()

    def add_reaction(self, guild_id, emote, role_id, channel_id, message_id):
        if not str(guild_id) in reaction_roles_data:
            reaction_roles_data[str(guild_id)] = []
        reaction_roles_data[str(guild_id)].append(
            {
                "id": str(uuid.uuid4()),
                "emote": emote,
                "roleID": role_id,
                "channelID": channel_id,
                "messageID": message_id,
            }
        )
        store_reaction_roles()

    def parse_reaction_payload(self, payload: discord.RawReactionActionEvent):
        guild_id = payload.guild_id
        data = reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            for rr in data:
                emote = rr.get("emote")
                if payload.message_id == rr.get("messageID"):
                    if payload.channel_id == rr.get("channelID"):
                        if str(payload.emoji) == emote:
                            guild = self.client.get_guild(guild_id)
                            role = guild.get_role(rr.get("roleID"))
                            user = guild.get_member(payload.user_id)
                            return role, user
        return None, None


async def setup(client):
    await client.add_cog(ReactionRoles(client))