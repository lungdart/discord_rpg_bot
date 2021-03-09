""" Shopping commands """
import os
from bot.components import users, stuff
from bot.api.errors import CommandError

class ShopAPI():
    """ Shop API utilizing caching """
    def __init__(self, parent):
        self._parent = parent

        self.weapons = []
        self.armor = []
        self.accessories = []
        self.items = []
        self.spells = []
        self.load_all()

    def load_all(self):
        """ Loads the shop form the disk """
        for entry in os.scandir(os.getenv('DATA_PATH')):
            if entry.is_file():
                # First word is the weapon type (category)
                file_no_ext = os.path.splitext(entry.name)[0]
                parts = file_no_ext.split("_")
                category = parts[0]

                fullpath = os.path.join(os.getenv('DATA_PATH'), entry.name)
                if category == 'sword':
                    self.weapons.append(stuff.Sword.load(fullpath))
                elif category == 'axe':
                    self.weapons.append(stuff.Axe.load(fullpath))
                elif category == 'bow':
                    self.weapons.append(stuff.Bow.load(fullpath))
                elif category == 'armor':
                    self.armor.append(stuff.Armor.load(fullpath))
                elif category == 'accessory':
                    self.accessories.append(stuff.Accessory.load(fullpath))
                else:
                    continue

    def create(self, **kwargs):
        """ Creates the appropriate instance from the saved dictionary """
        new = stuff.factory(**kwargs)
        if isinstance(new, stuff.Weapon):
            self.weapons.append(new)
        elif isinstance(new, stuff.Armor):
            self.armor.append(new)
        elif isinstance(new, stuff.Accessory):
            self.accessories.append(new)
        elif isinstance(new, stuff.Spell):
            self.spells.append(new)
        elif isinstance(new, stuff.Item):
            self.items.append(new)
        else:
            raise KeyError("Unknown item type")

    def list_all(self):
        """ List all items for sale """
        result = {
            'weapons'    : self.list_weapons(),
            'armor'      : self.list_armor(),
            'accessories': self.list_accessories(),
            'items'      : self.list_items(),
            'spells'     : self.list_spells(),
        }

        return result

    def list_weapons(self):
        """ List only weapons for sale """
        return [x.name for x in self.weapons]

    def list_armor(self):
        """ List only armor for sale """
        return [x.name for x in self.armor]

    def list_accessories(self):
        """ List only accessories for sale """
        return [x.name for x in self.accessories]

    def list_items(self):
        """ List only items for sale """
        return [x.name for x in self.items]

    def list_spells(self):
        """ List only spells for sale """
        return [x.name for x in self.spells]

    def find_info(self, name):
        """ Get the info for any item by name """
        if name in self.list_weapons():
            return self.weapon_info(name)
        if name in self.list_armor():
            return self.armor_info(name)
        if name in self.list_accessories():
            return self.accessory_info(name)
        if name in self.list_items():
            return self.item_info(name)
        if name in self.list_spells():
            return self.spell_info(name)
        raise CommandError(f"Couldn't find anything by the name {name} for sale")

    def weapon_info(self, name):
        """ Gets weapons info by name """
        for item in self.weapons:
            if item.name == name:
                return {
                    'name' : item.name,
                    'desc' : item.desc,
                    'power': item.power,
                    'value': item.value
                }

        raise CommandError(f"Couldn't find a weapon for sale by the name {name}")

    def armor_info(self, name):
        """ Gets armor info by name """
        for item in self.armor:
            if item.name == name:
                return {
                    'name'      : item.name,
                    'desc'      : item.desc,
                    'toughness' : item.toughness,
                    'value'     : item.value
                }

        raise CommandError(f"Couldn't find armor for sale by the name {name}")

    def accessory_info(self, name):
        """ Gets accessory info by name """
        for item in self.accessories:
            if item.name == name:
                return {
                    'name' : item.name,
                    'desc' : item.desc,
                    'value': item.value
                }

        raise CommandError(f"Couldn't find an accessory for sale by the name {name}")

    def item_info(self, name):
        """ Gets item info by name """
        for item in self.items:
            if item.name == name:
                return {
                    'name' : item.name,
                    'desc' : item.desc,
                    'value': item.value
                }

        raise CommandError(f"Couldn't find an item for sale by the name {name}")

    def spell_info(self, name):
        """ Gets spell info by name """
        for item in self.spells:
            if item.name == name:
                return {
                    'name' : item.name,
                    'desc' : item.desc,
                    'value': item.value
                }

        raise CommandError(f"Couldn't find a spell for sale by the name {name}")

    def buy(self, target, name, quantity=1):
        """ Buy an item from the for sale list """
        if quantity < 1:
            raise CommandError(f"{quantity} is an invalid quantity to purchase!")

        # Find the item
        if name in self.list_weapons():
            found = self.weapons
        elif name in self.list_armor():
            found = self.armor
        elif name in self.list_accessories():
            found = self.accessories
        elif name in self.list_items():
            found = self.items
        elif name in self.list_spells():
            found = self.spells
        else:
            raise CommandError(f"Couldn't find anything for sale by the name {name}")
        item = next((x for x in found if x.name == name))

        # Perform the transaction
        cost = item.value * quantity
        if not target.spend(cost):
            raise CommandError(f"{target.name} does not have enough gold to purchase {quantity}x {item.name}")
        target.give(item, quantity)

        # Save the character
        self._parent.character.save(target.name)

    def sell(self, target, name, quantity=1):
        """ Sell x item's from a users inventory """
        # Ensure user has enough to sell
        value = 0
        for entry in target.inventory:
            if entry['item'].name == name:
                value = entry['item'].value * quantity
                break

        # Do the transaction
        if not target.drop(name, quantity):
            raise CommandError(f"{target.name} doesn't have {quantity} {name} to sell")
        target.earn(value)

        # Save the character
        self._parent.character.save(target.name)
