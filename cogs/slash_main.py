import discord
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from datetime import datetime,timezone,timedelta

class Slash_main(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @cog_ext.cog_slash(name="test",description="一個測試的指令")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="測試測試",color=0xffffff)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ping",description="測試一下這個機器人的延遲")
    async def ping(self, ctx: SlashContext):
        embed = Embed(title="ping",color=0xffffff)
        ping = f"{round(self.bot.latency*1000)} ms"
        embed.add_field(name="第一次", value=ping, inline=True)
        m=await ctx.send("pong!",embed=embed)
        ping2 = f"{round(self.bot.latency*1000)} ms"
        embed.add_field(name="第二次", value=ping2, inline=True)
        await m.edit(embed=embed)

    @cog_ext.cog_slash(name="avatar",description="拿到某個人的頭像")
    async def avatar(self, ctx: SlashContext, *, member: discord.Member):
        userAvatarUrl = member.avatar_url
        embed=Embed(title="頭像連結",url=userAvatarUrl,color=0xffffff)
        embed.set_author(name=f"{member.name}")
        embed.set_image(url=f"{userAvatarUrl}")
        embed.set_footer(
            text=f"{ctx.author.name}",
            icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="time",description="報時")
    async def time(self,ctx: SlashContext):
      dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
      dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
      embed=discord.Embed(title="現在時間", color=0xffffff)
      embed.add_field(name="UTC", value=dt1, inline=False)
      embed.add_field(name="TW", value=dt2, inline=False)
      await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="server",description="關於伺服器")
    async def server(self ,ctx: SlashContext):
      name = str(ctx.guild.name)
      description = str(ctx.guild.description)

      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)
      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(title=name + " 伺服器資訊",
                          description=description,
                          color=0xffffff)
      embed.set_thumbnail(url=icon)
      embed.add_field(name="伺服器擁有者", value=owner, inline=True)
      embed.add_field(name="伺服器ID", value=id, inline=True)
      embed.add_field(name="地區", value=region, inline=True)
      embed.add_field(name="人數", value=memberCount, inline=True)
      embed.add_field(name='表情數量', value=len(ctx.guild.emojis))
      embed.add_field(name="加成狀態", value=(ctx.guild.premium_tier))
      embed.add_field(name="頻道總數", value=len(ctx.guild.channels), inline=True)
      embed.add_field(name="文字頻道", value=len(ctx.guild.text_channels))
      embed.add_field(name="語音頻道", value=len(ctx.guild.voice_channels))
      embed.add_field(name="身分組", value=len(ctx.guild.roles), inline=True)
      embed.add_field(name="創立於", value=(ctx.guild.created_at))

      await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="user",description="關於使用者")
    async def user(self, ctx: SlashContext, user: discord.Member):
        embed = discord.Embed(title="{}的資料".format(user), color=0xffffff)
        embed.add_field(name="名稱", value=user.name + "#" + user.discriminator, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="狀態", value=user.status, inline=True)
        embed.add_field(name="最高身分", value=user.top_role)
        embed.add_field(name="身分組", value=f"{len(user.roles)}個")
        embed.add_field(name="加入自", value=user.joined_at)   
        embed.add_field(name="創建自", value=user.created_at)
        embed.add_field(name="機器人?", value=user.bot)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)



def setup(bot: Bot):
    bot.add_cog(Slash_main(bot))