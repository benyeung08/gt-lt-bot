import discord
from discord.ext import commands

# discord_slash is the library I use for Button components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    ComponentContext,
    create_actionrow,
    create_button,
)

bot = commands.Bot(command_prefix="-", case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
    print("Bot is ready")

    global guild, ticket_category, ticket_mod_role, management_role  # one of the annoying things about Python...



# called whenever a button is pressed
@bot.event
async def on_component(ctx: ComponentContext):
    await ctx.defer(
        ignore=True
    )  # ignore, i.e. don't do anything *with the button* when it's pressed.

    ticket_created_embed = discord.Embed(
        title="Ticket Processed",
        description=f"""Hey {ctx.author.name}! Thanks for opening a ticket with us today, but before we transfer you through to a manager, we have to approve your ticket. We have this step in place to prevent bots and spam tickets.
        Please describe your enquiry and our team will approve it shortly. We thank you in advance for your patience.""",
    )

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.me: discord.PermissionOverwrite(view_channel=True),
        ticket_mod_role: discord.PermissionOverwrite(view_channel=True),
    }

    ticket = await ticket_category.create_text_channel(
        f"{ctx.author.name}-{ctx.author.discriminator}", overwrites=overwrites
    )

    await ticket.send(
        ctx.author.mention, embed=ticket_created_embed
    )  # ping the user who pressed the button, and send the embed


@bot.command()
@commands.has_permissions(administrator=True)
async def sendticket(ctx):
    embed = discord.Embed(
        title="Contact Support",
        description="Click the button below to open a ticket",
    )

    actionrow = create_actionrow(
        *[
            create_button(
                label="Open Ticket", custom_id="ticket", style=ButtonStyle.primary
            ),
        ]
    )

    await ctx.send(embed=embed, components=[actionrow])


@bot.command(aliases=["approve"])
@commands.has_permissions(administrator=True)
async def up(ctx):
    overwrites = {
        ctx.guild.me: discord.PermissionOverwrite(view_channel=True),
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ticket_mod_role: discord.PermissionOverwrite(view_channel=None),
        management_role: discord.PermissionOverwrite(view_channel=True),
    }
    await ctx.channel.edit(overwrites=overwrites)

    await ctx.channel.send(
        "Ticket Approved!\nYour ticket has been approved and has been transferred through to the Management Team. They will assist you further with your enquiry."
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def close(ctx):
    await ctx.channel.delete()


bot.run("token")