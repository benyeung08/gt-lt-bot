import discord
import datetime
from discord.ext import commands
from discord_components import Button,ButtonStyle

buttons = [
[
Button(style=ButtonStyle.grey, label= '1'),
Button(style=ButtonStyle.grey, label='2'),
Button(style=ButtonStyle.grey, label='3'),
Button(style=ButtonStyle.blue, label='x'),
Button(style=ButtonStyle.red, label='Exit')
],
[
Button(style=ButtonStyle.grey, label='4'),
Button(style=ButtonStyle.grey, label='5'),
Button(style=ButtonStyle.grey, label= '6'),
Button(style= ButtonStyle.blue, label= '÷'),
Button(style=ButtonStyle.red, label='←'),
],
[
Button(style=ButtonStyle.grey, label='7'),
Button(style=ButtonStyle.grey, label='8'),
Button(style= ButtonStyle.grey, label='9'),
Button(style=ButtonStyle.blue, label='+'),
Button(style=ButtonStyle.red, label='Clear')
],
[
Button(style=ButtonStyle.grey, label='00'),
Button(style=ButtonStyle.grey, label='0'),
Button(style=ButtonStyle.grey, label='.'),
Button(style=ButtonStyle.blue, label='-'),
Button(style=ButtonStyle.green, label=' =')
],
]

def calc(exp):
  o = exp.replace('x','*')
  o = o.replace('+','/')
  result = ''
  try:
    result = str(eval(o))
  except:
    result = 'An error Occoured'
  return result

class calculator(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def calc(self,ctx):
    m = await ctx.send("Loading Calculator")
    expression = None
    delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    e = discord.Embed(title = f"{ctx.author.name}\’s | {ctx.author.id}", description=expression,tirnestamp=delta)
    await m.edit("",components=buttons, embed=e)
    aid = ctx.author.id
    while m.created_at > delta:
      res = await self.bot.wait_for("button_click")
      if ctx.author.id == aid and m.created_at < delta:
        expression = e.description
      if expression == 'None' or expression == 'An error Occoured':
          expression = ''
      if res.component.label == 'Exit':
        await res.respond('Calculator Closed', type=7)
        break
      elif res.component.label == '←':
        expression = expression[:-1]
      elif res.component.label == 'Clear':
        expression = None
      elif res.component.label == '=':
        expression = calc(expression) 
      else:
        expression = res.component.label
      f = discord.Embed(title=f'{res.author.name} ‘s calculator | {res.author.id}', description=expression, timestamp=delta)
      await res.respond(embed=f, component=buttons,type=7)

def setup(bot):
  bot.add_cog(calculator(bot))