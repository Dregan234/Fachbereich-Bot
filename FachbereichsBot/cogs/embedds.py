import discord
from discord.ext import commands





class EmbedCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Embeds ready.")


    @commands.has_permissions(administrator=True)
    @commands.command(name="embed")
    async def embeds(self, ctx, title, mes):
        author = ctx.message.author
        embed = discord.Embed(title=title, description=mes, colour=0x0e6b0e)
        embed.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    @commands.has_permissions(administrator=True)
    @commands.command(name="line")
    async def line(self, ctx):
        await ctx.send("__                                                                                                     __")
        await ctx.message.delete()

async def setup(client):
    await client.add_cog(EmbedCog(client))