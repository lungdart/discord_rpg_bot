""" Shopping commands """
from bot.components import users, stuff
from bot.api.errors import CommandError

def list_all():
    """ List all items for sale """
    result = {
        'weapons'    : list_weapons(),
        'armor'      : list_armor(),
        'accessories': list_accessories(),
        'items'      : list_items(),
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

def list_spells():
    """ List only spells for sale """
    return [x.name for x in stuff.SPELLS]

def weapon_info(name):
    """ Gets weapons info by name """
    for item in stuff.WEAPONS:
        if item.name == name:
            return {
                'name' : item.name,
                'desc' : item.desc,
                'power': item.power,
                'value': item.value
            }

    raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

def armor_info(name):
    """ Gets armor info by name """
    for item in stuff.ARMOR:
        if item.name == name:
            return {
                'name'      : item.name,
                'desc'      : item.desc,
                'toughness' : item.toughness,
                'value'     : item.value
            }

    raise CommandError(f"Couldn't find armor for sale by the name {name}")

def accessory_info(name):
    """ Gets accessory info by name """
    for item in stuff.ACCESSORIES:
        if item.name == name:
            return {
                'name' : item.name,
                'desc' : item.desc,
                'value': item.value
            }

    raise CommandError(f"Couldn't find an accessory for sale by the name {name}")

def item_info(name):
    """ Gets item info by name """
    for item in stuff.ITEMS:
        if item.name == name:
            return {
                'name' : item.name,
                'desc' : item.desc,
                'value': item.value
            }

    raise CommandError(f"Couldn't find an item for sale by the name {name}")

def spell_info(name):
    """ Gets spell info by name """
    for item in stuff.SPELLS:
        if item.name == name:
            return {
                'name' : item.name,
                'desc' : item.desc,
                'value': item.value
            }

    raise CommandError(f"Couldn't find a spell for sale by the name {name}")

def buy(username, name, quantity=1):
    """ Buy an item from the for sale list """
    try:
        target = users.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {target} does not exist!")

    # Find the item
    if name in list_weapons():
        found = stuff.WEAPONS
    elif name in list_armor():
        found = stuff.ARMOR
    elif name in list_accessories():
        found = stuff.ACCESSORIES
    elif name in list_items():
        found = stuff.ITEMS
    elif name in list_spells():
        found = stuff.SPELLS
    else:
        raise CommandError(f"Couldn't find anything for sale by the name {name}")
    item = next((x for x in found if x.name == name))

    # Perform the transaction
    if not target.spend(item.value):
        raise CommandError(f"{username} does not have enough gold to purchase {quantity}x {item}")
    target.give(item, quantity)

def sell(username, name, quantity=1):
    """ Sell x item's from a users inventory """
    try:
        target = users.load(username)
    except FileNotFoundError:
        raise CommandError(f"Username {username} does not exist!")

    # Ensure user has enough to sell
    count = 0
    for entry in target.inventory:
        if entry['item'].name == name:
            count = entry['quantity']
            break

    if count < quantity:
        raise CommandError(f"{username} doesn't have {quantity}x {name} to sell")

    # Do the transaction
    target.drop(name, quantity)
    target.earn(item.value)
