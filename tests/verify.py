import string
import random
import json
import asyncio
from captcha.image import ImageCaptcha
import discord
from discord.ext import commands

class name(commands.Cog, description="雜項"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def vsetup(self, ctx, role:discord.Role):
      """"""
      with open("datas/verify.json", "r") as f:
        data = json.load(f)

      if str(ctx.guild.id) not in data:
        data[str(ctx.guild.id)] = {}
        data[str(ctx.guild.id)]['role'] = str(role.id)

        with open("datas/verify.json", "w") as f:
            json.dump(data, f)
        await ctx.send("完成")

    @commands.command()
    async def verify(self, ctx):
      """"""
      with open("datas/verify.json", "r") as f:
        data = json.load(f)
        user = ctx.author
      if str(ctx.guild.id) in data:
        #role = data[str(ctx.guild.id)]['role']  
        code=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(5))
        txt = code.lower()
        print(txt)
        img = ImageCaptcha()
        image = img.generate_image(txt)
        image.show()
        image.save('images/verify/code.jpg')
        class role:
                def id(self):
                        return data[str(ctx.guild.id)]['role']
        await ctx.send("請輸入驗證碼(全部小寫):", file=discord.File('images/verify/code.jpg'))
        try:
                imputcode = await self.bot.wait_for('message', timeout = 60.0)
        except asyncio.TimeoutError:
                await ctx.channel.send('時間到!請重新再式一次')
        if imputcode.content == txt:

                print(role)
                role.id = role
                await user.add_roles(role)
                await ctx.send("驗證成功!")                


      else:
        await ctx.send("還沒設定驗證")

def setup(bot):
    bot.add_cog(name(bot))