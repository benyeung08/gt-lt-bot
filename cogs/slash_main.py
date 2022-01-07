import discord
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

class Slash_main(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="測試測試",color=0xffffff)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        embed = Embed(title="ping",color=0xffffff)
        ping = f"{round(self.bot.latency*1000)} ms"
        embed.add_field(name="第一次", value=ping, inline=True)
        m=await ctx.send("pong!",embed=embed)
        ping2 = f"{round(self.bot.latency*1000)} ms"
        embed.add_field(name="第二次", value=ping2, inline=True)
        await m.edit(embed=embed)

    @cog_ext.cog_slash(name="avatar")
    async def avatar(self, ctx: SlashContext, *, member: discord.Member):
        userAvatarUrl = member.avatar_url
        embed=Embed(title="頭像連結",url=userAvatarUrl,color=0xffffff)
        embed.set_author(name=f"{member.name}")
        embed.set_image(url=f"{userAvatarUrl}")
        embed.set_footer(
            text=f"{ctx.author.name}",
            icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)



def setup(bot: Bot):
    bot.add_cog(Slash_main(bot))