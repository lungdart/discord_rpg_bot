import os
from discord.ext import commands as discord_commands
import discord
from bot.components.users import load as load_user
from bot.components.logger import LoggerFactory
import bot.api as api

### GLOBAL VARIABLES ###
CLIENT = discord_commands.Bot(command_prefix='!', intents=discord.Intents.all())
CHANNEL = None
BATTLE = None
LOGGER_FACTORY = None


### COMMAND HOOKS ###
@CLIENT.command()
async def battle(ctx, round_limit=None):
    """ Trigger to start a new battle """
    global BATTLE
    BATTLE = battle.Battle(LOGGER_FACTORY)
    battle.start(round_limit)


@CLIENT.command()
async def join(ctx):
    """ User joins the battle """
    if not BATTLE:
        logger = LOGGER_FACTORY(title="Error", color="error")
        logger.add("Bad Command", "There is no active battle to join")
        await logger.pm(ctx.author.name)

    try:
        BATTLE.join(ctx.author.name)
    except api.errors.CommandError as error:
        logger = LOGGER_FACTORY(title="Error", color="error")
        logger.add("Bad Command", str(error))
        await logger.pm(ctx.author.name)

@CLIENT.command()
async def stats(ctx, target=None):
    """ Get the stats for the context user or the target user """
    if not target:
        target = ctx.author.name

    info = api.character.stats(target)
    level = f"""
    Level: {info['level']}
    Experience: {info['experience']}"""

    derived = f"""
    Life: {info['current_life']}/{info['base_life']}
    Mana: {info['current_mana']}/{info['base_mana']}
    Speed: {info['current_speed']}/{info['base_speed']}"""

    core = f"""
    Body: {info['current_body']}/{info['base_body']}
    Mind: {info['current_mind']}/{info['base_mind']}
    Agility: {info['current_agility']}/{info['base_agility']}"""

    equipped = f"""
    Weapon: {info['weapon']}
    Armor: {info['armor']}
    Accessory: {info['accessory']}"""

    skills = ', '.join(info['skills'])
    spells = ', '.join(info['spells'])
    all_items = ', '.join(info['items'] + info['gear'])
    gold = f"{info['gold']:,} Gold"

    logger = LOGGER_FACTORY(title="{target} Stats")
    logger.add("Level", level)
    logger.add("Derived Stats", derived)
    logger.add("Core Stats", core)
    logger.add("Equipped", equipped)
    logger.add("Skills", skills)
    logger.add("Spells", spells)
    logger.add("All Items", all_items)
    logger.add("Gold", gold)
    logger.pm(ctx.author.name)

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

    global CHANNEL, LOGGER_FACTORY
    CHANNEL = CLIENT.get_channel(channel_id)
    LOGGER_FACTORY = LoggerFactory(CHANNEL)

    # Load in all users in the channel
    for member in CHANNEL.members:
        load_user(member.name)


def start_client(token):
    """ Starts the discord client using the given auth token """
    if not token:
        raise TypeError("Token can not be None")
    CLIENT.run(token, bot=True)
