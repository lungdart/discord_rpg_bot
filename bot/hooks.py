import os
from discord.ext import commands as discord_commands
import discord
from bot.components.users import load as load_user
from bot.components.logger import DiscordLogger
import bot.api as api

### GLOBAL VARIABLES ###
CLIENT = discord_commands.Bot(command_prefix='!', intents=discord.Intents.all())
CHANNEL = None
BATTLE = None
LOGGER = None


### COMMAND HOOKS ###
@CLIENT.command()
async def battle(ctx, *args):
    """ Trigger to start a new battle """
    # No arguments indicates starting a battle
    if not args:
        BATTLE.new()
    elif args[0] == "start":
        BATTLE.start()
    elif args[0] == "stop":
        BATTLE.stop()

    # Bad command
    else:
        out = LOGGER.entry()
        out.color("error")
        out.title(f"Bad battle command {args[0]}")
        out.desc("Did you mean to use one of the following valid commands instead")
        out.field(
            title="Commands",
            desc="""
                **!battle**: Begins a new battle
                **!battle *start* **: Starts a battle if there are enough participants
                **!battle *stop* **: Stops a battle at any point. All progress is lost
            """)
        out.buffer()

    # Send everything from the buffer
    await LOGGER.send_buffer()


@CLIENT.command()
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
async def stats(ctx, target=None):
    """ Get the stats for the context user or the target user """
    if not target:
        target = ctx.author.name

    try:
        info = api.character.stats(target)
    except api.errors.CommandError as error:
        out = LOGGER.entry()
        out.color('error')
        out.title('Command Error')
        out.desc(str(error))
        out.buffer()
        await LOGGER.send_buffer()
        return

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
    inventory = info['inventory']
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
async def attack(ctx, target):
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

    global CHANNEL, LOGGER, BATTLE
    CHANNEL = CLIENT.get_channel(channel_id)
    LOGGER = DiscordLogger(CHANNEL)
    BATTLE = api.battle.Battle(LOGGER)

    # Load in all users in the channel
    for member in CHANNEL.members:
        load_user(member.name)


def start_client(token):
    """ Starts the discord client using the given auth token """
    if not token:
        raise TypeError("Token can not be None")
    CLIENT.run(token, bot=True)
