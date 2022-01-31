import discord
from datetime import datetime,timezone,timedelta
from discord.ext import commands


class Main(commands.Cog, description="雜項"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        """BOT延遲"""
        await ctx.send(f"{round(self.bot.latency*1000)} ms")

    @commands.command()
    async def delete(self, ctx, num: int):
        """刪除訊息"""
        await ctx.channel.purge(limit=num + 1)

    @commands.command()
    async def say(self, ctx, *, msg):
        """說話"""
        await ctx.send(msg)

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        """頭像"""
        userAvatarUrl = member.avatar_url
        await ctx.send(userAvatarUrl)

    @commands.command()
    async def time(self,ctx):
      """報時"""
      dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
      dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
      embed=discord.Embed(title="現在時間", color=0xffffff)
      embed.add_field(name="UTC", value=dt1, inline=False)
      embed.add_field(name="TW", value=dt2, inline=False)
      await ctx.send(embed=embed)

    @commands.command()
    async def link(self,ctx):
      """連結"""
      async with ctx.typing():
        embed=discord.Embed(title=" ", color=0xffffff)
        embed.set_author(name="點我邀請機器人", url="https://discord.com/oauth2/authorize?client_id=881788746222157884&permissions=8&scope=bot",

        icon_url = "https://cdn.discordapp.com/avatars/881788746222157884/c509fe9813837da63278d08cdd39ddbb.webp?size=1024")
        await ctx.send(embed=embed)
        

    @commands.command()
    async def server(self ,ctx):
      """關於伺服器"""
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

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member=None):
        """關於使用者"""
        if user == None: ##if no user is inputted
            user = ctx.author ##defines user as the author of the message
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
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Main(bot))
