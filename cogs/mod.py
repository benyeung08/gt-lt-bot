import discord
import re
import asyncio
import json
import time
from io import BytesIO

from discord.ext import commands


# Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id

def timetext(name):
    """ Timestamp, but in text form """
    return f"{name}_{int(time.time())}.txt"

owners = [881312396784840744, 778193161322627102, 7788274635871092777]

async def check_permissions(ctx, perms, *, check=all):
    """ Checks if author has permissions to a permission """
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

async def prettyResults(ctx, filename: str = "Results", resultmsg: str = "Here's the results:", loop=None):
    """ A prettier way to show loop results """
    if not loop:
        return await ctx.send("The result was empty...")

    pretty = "\r\n".join([f"[{str(num).zfill(2)}] {data}" for num, data in enumerate(loop, start=1)])

    if len(loop) < 15:
        return await ctx.send(f"{resultmsg}```ini\n{pretty}```")

    data = BytesIO(pretty.encode('utf-8'))
    await ctx.send(
        content=resultmsg,
        file=discord.File(data, filename=timetext(filename.title()))
    )

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f"reason is too long ({len(argument)}/{reason_max})")
        return ret

def has_permissions(*, check=all, **perms):
    """ discord.Commands method to check if author has permissions """
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)

async def check_priv(ctx, member):
    """ Custom (weird) way to check permissions when handling moderation commands """
    try:
        # Self checks
        if member.id == ctx.author.id:
            return await ctx.send(f"You can't {ctx.command.name} yourself")
        if member.id == ctx.bot.user.id:
            return await ctx.send("So that's what you think of me huh..? sad ;-;")

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        # Now permission check
        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.send(f"I can't {ctx.command.name} my creator ;-;")
            else:
                pass
        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"You can't {ctx.command.name} the owner, lol")
        if ctx.author.top_role == member.top_role:
            return await ctx.send(f"You can't {ctx.command.name} someone who has the same permissions as you...")
        if ctx.author.top_role < member.top_role:
            return await ctx.send(f"Nope, you can't {ctx.command.name} someone higher than yourself.")
    except Exception:
        pass

def responsible(target, reason):
    """ Default responsible maker targeted to find user in AuditLogs """
    responsible = f"[ {target} ]"
    if not reason:
        return f"{responsible} no reason given..."
    return f"{responsible} {reason}"

def actionmessage(case, mass=False):
    """ Default way to present action confirmation in chat """
    output = f"**{case}** the user"

    if mass:
        output = f"**{case}** the IDs/Users"

    return f"✅ Successfully {output}"

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slowmode(self, ctx, seconds: int):
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(f"慢速模式設定為 {seconds} 秒!")

    @commands.command()
    @commands.guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ 踢出成員 """
        if await check_priv(ctx, member):
            return

        try:
            await member.kick(reason=responsible(ctx.author, reason))
            try:
                await member.send(f"你被{ctx.message.author}踢出{ctx.message.guild.name},原因:\n{reason}")
                await ctx.send(actionmessage("完成!"))
            except:
                await ctx.send(actionmessage("完成!"))
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """ 更改暱稱 """
        if await check_priv(ctx, member):
            return

        try:
            await member.edit(nick=name, reason=responsible(ctx.author, "利用指令更改"))
            message = f"成功把 **{member.name}** 的暱稱改成 **{name}**"
            if name is None:
                message = f"清除 **{member.name}** 的暱稱"
            await ctx.send(message)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason: str = None):
        """ 停權某個人 """
        m = ctx.guild.get_member(member)
        if m is not None and await check_priv(ctx, m):
            return

        try:
            await ctx.guild.ban(discord.Object(id=member), reason=responsible(ctx.author, reason))
            await member.send(f"你被{ctx.message.guild.name}的{ctx.message.author}停權,原因:\n{reason}")
            await ctx.send(actionmessage(f"{member}被{ctx.message.author}停權"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @has_permissions(ban_members=True)
    async def massban(self, ctx, reason: ActionReason, *members: MemberID):
        """ Mass bans multiple members from the server. """
        try:
            for member_id in members:
                await ctx.guild.ban(discord.Object(id=member_id), reason=responsible(ctx.author, reason))
            await ctx.send(actionmessage("massbanned", mass=True))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason: str = None):
        """ 解除停權某個人 """
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=responsible(ctx.author, reason))
            await ctx.send(actionmessage("完成!"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        """ 禁言成員 """
        if await check_priv(ctx, member):
            return

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("請建立一個身分組叫做 **Muted** 注意大小寫")

        try:
            await member.add_roles(muted_role, reason=responsible(ctx.author, reason))
            await ctx.send(actionmessage("完成"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """ 解除禁言成員 """
        if await check_priv(ctx, member):
            return

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("請建立一個身分組叫做 **Muted** 注意大小寫")

        try:
            await member.remove_roles(muted_role, reason=responsible(ctx.author, reason))
            await ctx.send(actionmessage("完成"))
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=["ar"])
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def announcerole(self, ctx, *, role: discord.Role):
        """ Makes a role mentionable and removes it whenever you mention the role """
        if role == ctx.guild.default_role:
            return await ctx.send("To prevent abuse, I won't allow mentionable role for everyone/here role.")

        if ctx.author.top_role.position <= role.position:
            return await ctx.send("It seems like the role you attempt to mention is over your permissions, therefore I won't allow you.")

        if ctx.me.top_role.position <= role.position:
            return await ctx.send("This role is above my permissions, I can't make it mentionable ;-;")

        await role.edit(mentionable=True, reason=f"[ {ctx.author} ] announcerole command")
        msg = await ctx.send(f"**{role.name}** is now mentionable, if you don't mention it within 30 seconds, I will revert the changes.")

        while True:
            def role_checker(m):
                if (role.mention in m.content):
                    return True
                return False

            try:
                checker = await self.bot.wait_for("message", timeout=30.0, check=role_checker)
                if checker.author.id == ctx.author.id:
                    await role.edit(mentionable=False, reason=f"[ {ctx.author} ] announcerole command")
                    return await msg.edit(content=f"**{role.name}** mentioned by **{ctx.author}** in {checker.channel.mention}")
                else:
                    await checker.delete()
            except asyncio.TimeoutError:
                await role.edit(mentionable=False, reason=f"[ {ctx.author} ] announcerole command")
                return await msg.edit(content=f"**{role.name}** was never mentioned by **{ctx.author}**...")


def setup(bot):
    bot.add_cog(Moderator(bot))