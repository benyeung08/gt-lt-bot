import os
import discord
import keep_alive
from discord import Intents
from discord_slash import SlashCommand
from discord.ext import commands
from pretty_help import PrettyHelp

owners = [881312396784840744, 7788274635871092777]
activity = discord.Activity(type=discord.ActivityType.playing, name="…什麼東西")
bot = commands.Bot(command_prefix="><", activity=activity, owner_ids = set(owners), intents=Intents.all())
ending_note = "使用 ><help 來顯示這個訊息\n這是一個幫助訊息，能列出所有指令，好讓你能輕鬆自在的使用這個機器人"
bot.help_command = PrettyHelp(color=0xffffff, ending_note=ending_note)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
#當機器人完成啟動時
async def on_ready():
	print('> 目前登入身份：', bot.user)
	print('> Bot is now running.')

@bot.command()
async def load(ctx, extension):
  """創作者專用"""
  is_owner = await ctx.bot.is_owner(ctx.author)
  if is_owner:
	  bot.load_extension(f'cogs.{extension}')
	  await ctx.send(f'載入{extension}完成')
  else:
    await ctx.send("你不能做這件事")

@bot.command()
async def unload(ctx, extension):
  """創作者專用"""
  is_owner = await ctx.bot.is_owner(ctx.author)
  if is_owner:
	  bot.unload_extension(f'cogs.{extension}')
	  await ctx.send(f'卸下{extension}完成')
  else:
    await ctx.send("你不能做這件事")

@bot.command()
async def reload(ctx, extension):
  """創作者專用"""
  is_owner = await ctx.bot.is_owner(ctx.author)
  if is_owner:
	  bot.reload_extension(f'cogs.{extension}')
	  await ctx.send(f'重新載入{extension}完成')
  else:
    await ctx.send("你不能做這件事")

@bot.command()
async def reloadall(ctx):
  """創作者專用"""
  is_owner = await ctx.bot.is_owner(ctx.author)
  if is_owner:
    for file in os.listdir("cogs"):
      if file.endswith(".py"):
        name = file[:-3]
        bot.reload_extension(f"cogs.{name}")
    await ctx.send("重新載入成功")
  else:
    await ctx.send("你不能做這件事")

#------------------------------------
@bot.command()
async def bug(ctx, desc=None, rep=None):
    user = ctx.author
    await ctx.author.send('```描述一下你找到的bug```')
    responseDesc = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300)
    description = responseDesc.content
    embed = discord.Embed(title='BUG回報', color=0x00ff00)
    embed.add_field(name='描述', value=description, inline=False)
    embed.add_field(name='回報者:', value=user, inline=True)
    adminBug = bot.get_channel(934325021571154021)
    await adminBug.send(embed=embed)
    await ctx.author.send('OK!')
    # Add 3 reaction (different emojis) here
#------------------------------------

for Filename in os.listdir('./cogs'):
	if Filename.endswith('.py'):
		bot.load_extension(f'cogs.{Filename[:-3]}')

if __name__ == "__main__":
	keep_alive.keep_alive()
	bot.run(os.environ['TOKEN'])
    #TOKEN HERE