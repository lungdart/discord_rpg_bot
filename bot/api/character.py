""" Passive character commands """
from bot.components import user
from bot.api.errors import CommandError

def stats(username):
    """ Get the stats for the target user """
    # User stats are not private information. Anyone can request it
    try:
        target = user.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    result = {
        'username'       : target.name,
        'level'          : target.level,
        'experience'     : target.experience,
        'base_life'      : target.life.base,
        'current_life'   : target.life.current,
        'base_mana'      : target.mana.base,
        'current_mana'   : target.mana.current,
        'base_speed'     : target.speed.base,
        'current_speed'  : target.speed.current,
        'base_body'      : target.body.base,
        'current_body'   : target.body.current,
        'base_mind'      : target.mind.base,
        'current_mind'   : target.mind.current,
        'base_agility'   : target.agility.base,
        'current_agility': target.agility.current,
        'weapon'         : target.weapon.name,
        'armor'          : target.armor.name,
        'accessory'      : target.accessory.name,
        'skills'         : [x.name for x in target.skills],
        'spells'         : [x.name for x in target.spells],
        'items'          : [x.name for x in target.items],
        'gear'           : [x.name for x in target.gear],
        'gold'           : target.gold
    }

    return result

def equip(username, item):
    """ Equip an item """
    try:
        target = user.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    try:
        target.equip(item)
    except LookupError:
        raise CommandError(f"Could not find {item} in your inventory")
    except ValueError:
        raise CommandError(f"Equipping {item} doesn't make much sense...")

def unequip(username, slot):
    """ Unequip anything in a slot """
    try:
        target = user.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    try:
        target.unequip(slot)
    except ValueError:
        raise CommandError(f"Invalid equipment slot: {slot}")
