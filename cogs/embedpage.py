import discord
import asyncio
from discord.ext import commands

# help pages
page1 = discord.Embed(title="Bot Help 1", description="Use the buttons below to navigate between help pages.", colour=0xffffff)
page2 = discord.Embed(title="Bot Help 2", description="Page 2", colour=0xffffff)
page3 = discord.Embed(title="Bot Help 3", description="Page 3", colour=0xffffff)

pages = [page1, page2, page3]

class embedpage(commands.Cog, description="tests"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def page(self, ctx):
      buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9",u"\u274C"] # skip to start, left, right, skip to end
      current = 0
      msg = await ctx.send(embed=pages[current])
    
      for button in buttons:
        await msg.add_reaction(button)
        
      while True:
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=30.0)

        except asyncio.TimeoutError:
             try:
               await msg.delete()
             except:
               return

        else:
            if reaction.emoji == u"\u23EA":
                current = 0
                await msg.edit(embed=pages[current])
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    await msg.edit(embed=pages[current])
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(pages)-1:
                    current += 1
                    await msg.edit(embed=pages[current])

            elif reaction.emoji == u"\u23E9":
                current = len(pages)-1
                await msg.edit(embed=pages[current])

            elif reaction.emoji == u"\u274C":
              await msg.delete()

def setup(bot):
  bot.add_cog(embedpage(bot))