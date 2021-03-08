""" Hooks the API into discord commands """
import os
import functools
from discord.ext import commands as discord_commands
import discord
from bot.components.users import load as load_user, create as create_user
from bot.components.stuff import load_all as load_shop
from bot.components.logger import DiscordLogger
import bot.api as api

### GLOBAL VARIABLES ###
CLIENT = discord_commands.Bot(command_prefix='!', intents=discord.Intents.all())
CHANNEL = None
BATTLE = None
LOGGER = None


### Error handling decorators ###
def log_errors(func):
    """ Automatically logs errors correctly """
    @functools.wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        try:
            return await func(ctx, *args, **kwargs)
        except api.errors.CommandError as error:
            out = LOGGER.entry()
            out.color('error')
            out.title('Command Error')
            out.desc(str(error))
            out.buffer_pm(ctx.author.name)
            await LOGGER.send_buffer()
            return
        except Exception as error:
            out = LOGGER.entry()
            out.color('error')
            out.title('Unhandled Exception')
            out.desc(str(error))
            out.buffer()
            await LOGGER.send_buffer()
            raise error
    return wrapper



### COMMAND HOOKS ###
@CLIENT.command()
@log_errors
async def battle(ctx, command):
    """ Trigger to start a new battle """
    # No arguments indicates starting a battle
    if not command:
        BATTLE.new()
    elif command == "start":
        BATTLE.start()
    elif command == "stop":
        BATTLE.stop()
    elif command == "list":
        out = LOGGER.entry()
        out.title("Battle list")
        out.desc("Remember that the names are case sensitive when issuing battle actions!")
        out.field(
            title="Participants",
            desc="\n".join(BATTLE.participants))

    # Bad command
    else:
        out = LOGGER.entry()
        out.color("error")
        out.title(f"Bad battle command {command}")
        out.desc("Did you mean to use one of the following valid commands instead")
        out.field(
            title="Commands",
            desc="""
                **!battle**: Begins a new battle
                **!battle *list* **: Lists battle participants
                **!battle *start* **: Starts a battle if there are enough participants
                **!battle *stop* **: Stops a battle at any point. All progress is lost
            """)
        out.buffer()

    # Send everything from the buffer
    await LOGGER.send_buffer()


@CLIENT.command()
@log_errors
async def join(ctx):
    """ User joins the battle """
    if BATTLE.is_joinable:
        BATTLE.join(ctx.author.name)
    else:
        log = LOGGER.entry()
        log.color("warn")
        log.title("There is no battle ready to join")
        log.desc("Wait for a new battle to be ready for participants")
        log.buffer_pm(ctx.author.name)

    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
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

    power_tough = f"{info['power']}/{info['toughness']}"

    spells = ', '.join(info['spells']) if info['spells'] else 'Empty'
    inventory = "\n".join(info['inventory']) if info['inventory'] else 'None'
    gold = f"{info['gold']:,} Gold"

    out = LOGGER.entry()
    out.title(f"Stats for {target}")
    out.field(title="Level", desc=level)
    out.field(title="Derived Stats", desc=derived)
    out.field(title="Core Stats", desc=core)
    out.field(title="Equipped", desc=equipped)
    out.field(title="Power/Toughness", desc=power_tough)
    out.field(title="Spells", desc=spells)
    out.field(title="Inventory", desc=inventory)
    out.field(title="Gold", desc=gold)
    out.buffer_pm(ctx.author.name)
    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def shop(ctx):
    """ View all items available in the shop """
    stuff = api.shop.list_all()
    weapons     = '\n'.join(stuff['weapons']) if stuff['weapons'] else 'None'
    armor       = '\n'.join(stuff['armor']) if stuff['armor'] else 'None'
    accessories = '\n'.join(stuff['accessories']) if stuff['accessories'] else 'None'
    items       = '\n'.join(stuff['items']) if stuff['items'] else 'None'
    spells      = '\n'.join(stuff['spells']) if stuff['spells'] else 'None'

    out = LOGGER.entry()
    out.title('Welcome to the shop!')
    out.desc('Type *!info <ITEM>* to get more information about each item')
    out.field('Weapons', f'{weapons}')
    out.field('Armor', f'{armor}')
    out.field('Accessories', f'{accessories}')
    out.field('Items', f'{items}')
    out.field('Spells', f'{spells}')
    out.buffer_pm(ctx.author.name)
    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def info(ctx, *name):
    """ Get detailed information about an item """
    # Convert all additional parameters as a single name with spaces
    name = ' '.join(name)
    details = api.shop.find_info(name)

    # Parse the name and description as the embed title instead of a field
    out = LOGGER.entry()
    out.title(f"{details['name']}")
    out.desc(f"{details['desc']}")

    # Parse the rest of the attributes as fields
    del details['name']
    del details['desc']
    for key in details:
        out.field(title=f'{key}', desc=f'{details[key]}')
    out.buffer_pm(ctx.author.name)

    await LOGGER.send_buffer()


@CLIENT.command()
@log_errors
async def buy(ctx, *args):
    """ Purchase an item by name from the shop """
    # Try to get the quantity as the final argument
    try:
        quantity = int(args[-1])
        args = args[:-1]
    except ValueError:
        quantity = 1

    # Get the full name of the item to buy as the rest of the arguments
    name = ' '.join(args)

    api.shop.buy(ctx.author.name, name, quantity)

    out = LOGGER.entry()
    out.color('success')
    out.title(f"{name} purchased!")
    out.desc(f"You pruchased {name} and are much poorer")
    out.buffer_pm(ctx.author.name)
    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def sell(ctx, name, quantity=1):
    """ Sell an item by name form your inventory """

@CLIENT.command()
@log_errors
async def equip(ctx, *name):
    """ Equip a gear item into it's appropriate slot """
    # Converts multi word names into a single argument
    name = ' '.join(name)
    api.character.equip(ctx.author.name, name)

    out = LOGGER.entry()
    out.color('success')
    out.title(f"You equipped {name}")
    out.buffer_pm(ctx.author.name)
    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def unequip(ctx, slot):
    """ Unequip the item in the slot """

@CLIENT.command()
@log_errors
async def attack(ctx, target):
    """ Have the author attack the target """
    if BATTLE.is_round_wait:
        BATTLE.submit_action(ctx.author.name, 'attack', target=target)
    else:
        log = LOGGER.entry()
        log.color("warn")
        log.title("There is no battle round waiting for turn actions")
        log.desc("Wait for the next round, or the next battle")
        log.buffer_pm(ctx.author.name)

    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def defend(ctx):
    """ Have the user defend for the turn """
    if BATTLE.is_round_wait:
        BATTLE.submit_action(ctx.author.name, 'defend')
    else:
        log = LOGGER.entry()
        log.color("warn")
        log.title("There is no battle round waiting for turn actions")
        log.desc("Wait for the next round, or the next battle")
        log.buffer_pm(ctx.author.name)

    await LOGGER.send_buffer()

@CLIENT.command()
@log_errors
async def magic(ctx, spell, target=None):
    """ Have the author cast a spell on the target """

@CLIENT.command()
@log_errors
async def item(ctx, spell, target=None):
    """ Have the author use an item on a target """


### STARTING THE CLIENT ###
@CLIENT.event
async def on_ready():
    print(f'{CLIENT.user} connected')

    # Fetch all members in the battle channel
    channel_id = int(os.getenv('DISCORD_CHANNEL'))

    global CHANNEL, LOGGER, BATTLE
    CHANNEL = CLIENT.get_channel(channel_id)
    LOGGER = DiscordLogger(CHANNEL)
    BATTLE = api.battle.Battle(LOGGER)

    # Load in all users in the channel
    for member in CHANNEL.members:
        try:
            load_user(member.name)
        except FileNotFoundError:
            create_user(member.name)

    # Load all shop items
    load_shop()


def start_client(token):
    """ Starts the discord client using the given auth token """
    if not token:
        raise TypeError("Token can not be None")
    CLIENT.run(token, bot=True)
