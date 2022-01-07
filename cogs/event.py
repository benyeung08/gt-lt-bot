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
      
    if message.content == 'hi':
      tmp=["hi","hihi","嗨","嗨嗨"]
      await message.channel.send(tmp[random.randint(0,3)])

    if message.content == '安安':
      tmp=["安安阿","安安","你好","你好!"]
      await message.channel.send(tmp[random.randint(0,3)])
  @commands.Cog.listener(name='on_command')
  async def print(self, ctx):
    server = ctx.guild.name
    user = ctx.author
    command = ctx.message.content
    print(f'{server} > {user} > {command}')


def setup(bot):
  bot.add_cog(Event(bot))