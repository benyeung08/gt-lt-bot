import discord
import random
from discord.ext import commands

class Event(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self,message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == self.bot.user:
      return
    try:
      if message.content == 'hi' or message.content == 'hello':
        tmp=["hi","hihi","嗨","嗨嗨","hello","hello there","哈囉"]
        await message.channel.send(random.choice(tmp))

      if message.content == '安安':
        tmp=["安安阿","安安","你好","你好!","嗨"]
        await message.channel.send(random.choice(tmp))
    except:
      return
    if self.bot.user.mentioned_in(message):
      if message.content == '<@!881788746222157884>':
        await message.channel.send(" 打上`><help`來看看有什麼神奇的功能吧! ")

  @commands.Cog.listener(name='on_command')
  async def print(self, ctx):
    server = ctx.guild.name
    user = ctx.author
    command = ctx.message.content
    msg = f'{server} > {user} > {command}'
    ch = self.bot.get_channel(944767818375782441)
    await ch.send(msg)
    print(msg)


def setup(bot):
  bot.add_cog(Event(bot))