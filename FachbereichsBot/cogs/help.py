import discord
from discord.ext import commands

class HelpCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Help ready.")
    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(tile = 'Help Commands', description='Hier sind alle Commands auf die ich reagiere: ', colour=0x0e6b0e)
        embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
        embed.add_field(name="Reaction Roles", value='!ra\n'
                                                     '!reaction\n'
                                                     '!reactions\n'
                                                     '!rr\n'
                                                     '!removeall\n'
                                                     'Für eine genauere Hilfe !reactionhelp'
                        )
        embed.add_field(name="Embeds", value="!embed <Titel> <Beschreibung>")
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def reactionhelp(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(tile = "Reaction Commands", description="Hier sind alle Reaction Commands genauer beschrieben", colour=0x0e6b0e)
        embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
        embed.add_field(name="!ra", value="Hiermit kann zu einer bereits bestehenden Nachricht eine Reaction-Role hinzugefügt werden\n\n"
                                          "!ra <emote> <role> <channel> <message_id>")
        embed.add_field(name="!reaction", value="Hiermit kann eine neue Reaction-Role durch den Bot in Form eines Embeds erstellt werden.\n\n"
                                                "!reaction <emote> <role> <channel> <title> <message>")
        embed.add_field(name="!reactions", value="Hiermit können alle vorhandenen Reaction-Roles angezeigt werden")
        embed.add_field(name="!rr", value="Hiermit können bereits vorhandene Reaction-Roles gelöscht werden.\n\n"
                                          "!rr <index>")
        embed.add_field(name="!removeall",value="Hiermit werden alle Reaktionen des Servers bis auf die des Bots entfernt")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpCog(client))