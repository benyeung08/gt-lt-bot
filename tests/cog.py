import discord
from discord.ext import commands


class name(commands.Cog, description="雜項"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(name(bot))