""" User object """
import os
import json
from bot.components.stats import CoreStat, DerivedStat
from bot.components.stuff import Stuff, Gear


### GLOBALS
CACHE = {}


### CLASS DEFINITIONS
class User():
    """ User object """
    def __init__(self, name):
        # Meta data
        self.name = name
        self.level = 1
        self.experience = 0

        # Stats
        self.body = None
        self.mind = None
        self.agility = None
        self.life = None
        self.mana = None
        self.speed = None

        # Stuff
        self.weapon = None
        self.armor = None
        self.accessory = None
        self.spells = []
        self.inventory = []
        self._gold = 0

        # Battle statuses
        self.defending = False

    @classmethod
    def create(cls, name):
        """ Creates a new user with default values """
        this = cls(name)

        # Core stats
        this.body = CoreStat(1)
        this.mind = CoreStat(1)
        this.agility = CoreStat(1)
        this._derive_stats()

        return this

    @classmethod
    def load(cls, name):
        """ Load user from disk """
        filename = os.path.join(os.getenv('DATA_PATH'), f'user_{name}.json')
        with open(filename, 'r') as file:
            data = json.load(file)

        this = cls(name)
        this.level = data["level"]
        this.experience = data["experience"]

        this.body = CoreStat(data["body"])
        this.mind = CoreStat(data["mind"])
        this.agility = CoreStat(data["agility"])
        this._derive_stats()

        this.weapon = data["weapon"]
        this.armor = data["armor"]
        this.accessory = data["accessory"]

        this.inventory = data["inventory"]
        # this.items = data["items"]
        # this.spells = data["spells"]

        this._gold = data["gold"]

        return this

    def save(self):
        """ Saves this user to disk """
        filename = os.path.join(os.getenv('DATA_PATH'), f'user_{self.name}.json')
        data = UserEncoder().encode(self)

        with open(filename, 'w') as file:
            file.write(data)

    def restore(self):
        """ Restores this user back to base line """
        self.body.restore()
        self.mind.restore()
        self.agility.restore()

        self.life.restore()
        self.mana.restore()
        self.speed.restore()

    @property
    def gold(self):
        return self._gold

    def earn(self, amount):
        """ Earn new monies """
        self._gold += amount

    def spend(self, amount):
        """ Spend old monies """
        if self._gold >= amount:
            self._gold -= amount
            return True

        return False

    def give(self, item, quantity=1):
        """ Give this user a new item """
        if not isinstance(item, Stuff):
            return False

        # Increment quantity if you already have it
        for entry in self.inventory:
            if entry['item'].name == item.name:
                entry['quantity'] += quantity
                return True

        # Create a new entry with the quantity given
        entry = {'item': item, 'quantity': quantity}
        self.inventory.append(entry)
        return True

    def drop(self, name, quantity=1):
        """ Drop items from your inventory forever """
        # Early out if user doesn't have the item to drop
        idx = None
        for i in range(len(self.inventory)):
            if self.inventory[i]['item'].name == name:
                idx = i
                break
        if idx is None or self.inventory[idx]['quantity'] < quantity:
            return False

        # Remove item completely if it's the last one dropped
        if self.inventory[idx]['quantity'] == quantity:
            del self.inventory[idx]
        else:
            self.inventory[idx]['quantity'] -= quantity

        return True

    def equip(self, item):
        """ Equip the item """
        if not isinstance(item, Gear):
            return False

        # Change the equipment slot to match
        if item.slot == "weapon":
            self.unequip("weapon")
            self.weapon = item
        elif item.slot == "armor":
            self.unequip("armor")
            self.armor = item
        elif item.slot == "accessory":
            self.unequip("accessory")
            self.accessory = item
        else:
            return False

        # Remove the equipped item from the inventory if it exists, it's still okay if it didn't
        idx = None
        for i in range(len(self.inventory)):
            if self.inventory[i]['item'].name == item.name:
                idx = i
                break
        if idx is None:
            return True

        self.inventory[idx]['quantity'] -= 1
        if self.inventory[idx]['quantity'] < 1:
            del self.inventory[idx]
        return True

    def unequip(self, slot_name):
        """ Unequip whatever is in that slot and put it back in users inventory """
        item = None
        if slot_name == "weapon":
            item = self.weapon
            self.weapon = None
        elif slot_name == "armor":
            item = self.armor
            self.armor = None
        elif slot_name == "accessory":
            item = self.accessory
            self.accessory = None
        else:
            return False

        if item:
            self.give(item, 1)
        return True

    def is_alive(self):
        """ Checks if this user is dead or alive """
        return self.life.current > 0

    def _derive_stats(self):
        """ Generates the derived stats from the core stats """
        self.life = DerivedStat(self.body, factor=25, offset=100)
        self.mana = DerivedStat(self.mind, factor=5, offset=5)
        self.speed = DerivedStat(self.agility, factor=2, offset=0)


class UserEncoder(json.JSONEncoder):
    """ A custom JSON encoder that understands our user objects """
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'name'      : obj.name,
                'level'     : obj.level,
                'experience': obj.experience,
                'body'      : obj.body.base,
                'mind'      : obj.mind.base,
                'agility'   : obj.agility.base,
                'weapon'    : obj.weapon,
                'armor'     : obj.armor,
                'accessory' : obj.accessory,
                'spells'    : obj.spells,
                'inventory' : obj.inventory,
                'gold'      : obj.gold
            }

        else:
            return json.JSONEncoder.default(self, obj)


### USER FETCHING
def create(name):
    """ Creates a new user and saves to disk """
    user = User.create(name)
    CACHE[name] = user
    user.save()

    return user

def load(name):
    """ Get's the named user instance """
    # Fetch user from cache first
    try:
        user = CACHE[name]
        return user
    except KeyError:
        pass

    # If their not in cache, load from disk. (Will throw FileNotFound error if missing)
    user = User.load(name)
    CACHE[name] = user

    return user

def unload(name):
    """ Save then unload a user from cache """
    try:
        # Try to save the user first
        user = CACHE[name]
        user.save()

        # Remove from cache
        del CACHE[name]

    except KeyError:
        # User wasn't loaded, ignore
        pass
