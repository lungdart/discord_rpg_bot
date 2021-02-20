import os
from discord.ext import commands as discord_commands
import discord
from bot import actions
from bot.components.users import load as load_user

### GLOBAL VARIABLES ###
CLIENT = discord_commands.Bot(command_prefix='!', intents=discord.Intents.all())


### COMMAND HOOKS ###
@CLIENT.command()
async def battle(ctx, *args):
    pass

@CLIENT.command()
async def join(ctx, *args):
    pass

@CLIENT.command()
async def stats(ctx):
    print(type(ctx.author))
    result = actions.get_stats(ctx.author.name)
    await ctx.send(embed=result)

@CLIENT.command()
async def shop(ctx, *args):
    pass

@CLIENT.command()
async def buy(ctx, *args):
    pass

@CLIENT.command()
async def items(ctx, *args):
    pass

@CLIENT.command()
async def equip(ctx, *args):
    pass

@CLIENT.command()
async def attack(ctx, *args):
    pass

@CLIENT.command()
async def defend(ctx, *args):
    pass

@CLIENT.command()
async def magic(ctx, *args):
    pass

@CLIENT.command()
async def item(ctx, *args):
    pass


### STARTING THE CLIENT ###
@CLIENT.event
async def on_ready():
    print(f'{CLIENT.user} connected')

    # Fetch all members in the battle channel
    channel_id = int(os.getenv('DISCORD_CHANNEL'))
    channel = CLIENT.get_channel(channel_id)
    members = channel.members

    # Load in all users in the channel
    for member in members:
        load_user(member.name)


def start_client(token):
    """ Starts the discord client using the given auth token """
    if not token:
        raise TypeError("Token can not be None")
    CLIENT.run(token, bot=True)
