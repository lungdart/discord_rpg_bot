from bot.components import stuff
from bot.api.errors import CommandError

def list_all():
    """ List all items for sale """
    result = {
        'weapons'    : list_weapons(),
        'armor'      : list_armor(),
        'accessories': list_accessories(),
        'items'      : list_items(),
        'skills'     : list_skills(),
        'spells'     : list_spells(),
    }

    return result

def list_weapons():
    """ List only weapons for sale """
    return [x.name for x in stuff.WEAPONS]

def list_armor():
    """ List only armor for sale """
    return [x.name for x in stuff.ARMOR]

def list_accessories():
    """ List only accessories for sale """
    return [x.name for x in stuff.ACCESSORIES]

def list_items():
    """ List only items for sale """
    return [x.name for x in stuff.ITEMS]

def list_skills():
    """ List only skills for sale """
    return [x.name for x in stuff.SKILLS]

def list_spells():
    """ List only spells for sale """
    return [x.name for x in stuff.SPELLS]

def weapon_info(name):
    """ Gets weapons info by name """
    for item in stuff.WEAPONS:
        if item.name == name
            return {
                'name'       : item.name,
                'description': item.description,
                'power'      : item.power,
                'value'      : item.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def armor_info(name):
    """ Gets armor info by name """
    for item in stuff.ARMOR:
        if item.name == name
            return {
                'name'       : weapon.name,
                'description': weapon.description,
                'power'      : weapon.power,
                'value'      : weapon.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def weapon_info(name):
    """ Gets weapons info by name """
    for weapon in stuff.WEAPONS:
        if weapon.name == name
            return {
                'name'       : weapon.name,
                'description': weapon.description,
                'power'      : weapon.power,
                'value'      : weapon.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def weapon_info(name):
    """ Gets weapons info by name """
    for weapon in stuff.WEAPONS:
        if weapon.name == name
            return {
                'name'       : weapon.name,
                'description': weapon.description,
                'power'      : weapon.power,
                'value'      : weapon.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def weapon_info(name):
    """ Gets weapons info by name """
    for weapon in stuff.WEAPONS:
        if weapon.name == name
            return {
                'name'       : weapon.name,
                'description': weapon.description,
                'power'      : weapon.power,
                'value'      : weapon.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def weapon_info(name):
    """ Gets weapons info by name """
    for weapon in stuff.WEAPONS:
        if weapon.name == name
            return {
                'name'       : weapon.name,
                'description': weapon.description,
                'power'      : weapon.power,
                'value'      : weapon.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def buy(username, item):
    """ Buy an item from the for sale list """
    pass

def sell(username, item, quanitity):
    """ Sell x item's from a users inventory """
    pass
