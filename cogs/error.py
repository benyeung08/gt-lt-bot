import discord
import math,sys,traceback
from discord.ext import commands

class Error(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("沒這指令啦!(CommandNotFound)")
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '我需要 **{}** 的權限.(BotMissingPermissions)'.format(fmt)
            await ctx.send(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send('指令已停用(DisabledCommand)')
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("指令還在冷卻， {} 秒後再式一次.(CommandOnCooldown)".format(math.ceil(error.retry_after)))
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, 和 {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' 和 '.join(missing)
            _message = '你需要 **{}** 的權限(MissingPermissions)'.format(fmt)
            await ctx.send(_message)
            return

        if isinstance(error, commands.UserInputError):
            await ctx.send("輸入錯誤(UserInputError)")
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send('這個指令不能用在私訊(NoPrivateMessage)')
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send("你沒有權限(CheckFailure)")
            return

        # ignore all other exception types, but print them to stderr
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

        try:
          await ctx.send('發生錯誤，請再式一次或使用 `><bug` 來回報\n錯誤訊息: \n Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        except:
          await ctx.send("發生錯誤，無法傳送錯誤訊息，請再式一次或使用 `><bug` 來回報")

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
  bot.add_cog(Error(bot))