""" Passive character commands """
from bot.components import users
from bot.api.errors import CommandError

def stats(username):
    """ Get the stats for the target user """
    # User stats are not private information. Anyone can request it
    try:
        target = users.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {username} does not exist!")
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
        'weapon'         : target.weapon.name if target.weapon else 'Empty',
        'armor'          : target.armor.name if target.armor else 'Empty',
        'accessory'      : target.accessory.name if target.accessory else 'Empty',
        'power'          : target.weapon.power if target.weapon else 1,
        'toughness'      : target.armor.toughness if target.armor else 1,
        'spells'         : [x.name for x in target.spells],
        'inventory'      : [x['item'].name for x in target.inventory],
        'gold'           : target.gold
    }

    return result

def equip(username, name):
    """ Equip an item by name"""
    try:
        target = users.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    item = None
    for entry in target.inventory:
        if entry['item'].name == name:
            item = entry['item']
    if item is None:
        raise CommandError(f"Could not find {name} in {username}'s inventory")

    if not target.equip(item):
        raise CommandError(f"Could not equip {name}")

def unequip(username, slot):
    """ Unequip anything in a slot """
    try:
        target = users.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    if not target.unequip(slot):
        raise CommandError(f"Invalid equipment slot: {slot}")
