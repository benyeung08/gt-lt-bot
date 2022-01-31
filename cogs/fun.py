import random
from discord.ext import commands

list1 = ["肯定的", "確實如此", "毫無疑問", "是的, 肯定的", "您可以信賴它", "最有可能", "在我看來，是的", "是", "標誌指向是", "等下再問", "再試一次", "現在最好不要告訴你", "現在不能告訴你", "集中注意力再問一次", "不要指望它", "我的答案是否定的", "我的消息來源說不", "非常可疑", "展望 不太好"]

class Fun(commands.Cog, description="好玩的東西"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='8ball',
        description='一個8ball?',
        aliases=['8b'],
    )
    async def ball_command(self, ctx, *, question = None):
        """一個8ball?"""
        if question is None:
            await ctx.reply('這裡啥都沒!')
        else:
            await ctx.reply(random.choice(list1))

        return

    @commands.command(
        name='choice',
        description='幫你選擇個東西',
        aliases=['choose', 'pick'],
    )
    async def choice_command(self, ctx, *choices : str):
        """幫你選擇個東西"""
        try:
            await ctx.send(f"我選... {random.choice(choices)} !")
        except:
            await ctx.send('我什麼也沒選')

        return
def setup(bot):
    bot.add_cog(Fun(bot))