import os
import json
import random


### GLOBALS
WEAPONS = []
ARMOR = []
ACCESSORIES = []
ITEMS = []
SKILLS = []
SPELLS = []

### CLASSES
class Stuff():
    _prefix = None

    """ Base class, do not use directly """
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.desc = kwargs['desc']
        self.category = kwargs['category']
        self.value = kwargs.get('value', 0)

    @classmethod
    def load(cls, name):
        """ Load user from disk """
        filename = os.path.join(os.getenv('DATA_PATH'), f'{cls._prefix}_{name}.json')
        with open(filename, 'r') as file:
            data = json.load(file)

        this = cls(**data)
        return this

    def save(self):
        """ Saves this user to disk """
        filename = os.path.join(os.getenv('DATA_PATH'), f'{self._prefix}_{self.name}.json')
        data = json.dumps(self.__dict__)

        with open(filename, 'w') as file:
            file.write(data)


# EQUIPMENT
class Gear(Stuff):
    """ Base class, do not use directly """
    def __init__(self, **kwargs):
        kwargs['category'] = "gear"
        super(Gear, self).__init__(**kwargs)

        self.slot = kwargs['slot']

class Weapon(Gear):
    """ Base class, do not use directly """
    def __init__(self, **kwargs):
        kwargs['slot'] = "weapon"
        super(Weapon, self).__init__(**kwargs)

        self.type = kwargs['type']
        self.power = kwargs['power']
        self.min_factor = kwargs['min_factor']
        self.max_factor = kwargs['max_factor']

    def calc_power(self):
        """ Calculates the random weapon power fluctuation """
        low = int(self.power * self.min_factor)
        high = int(self.power * self.max_factor)
        power = random.randint(low, high)

        return power

class Sword(Weapon):
    _prefix = "sword"

    def __init__(self, **kwargs):
        kwargs['type'] = "sword"
        kwargs['min_factor'] = 0.8
        kwargs['max_factor'] = 1.0
        super(Sword, self).__init__(**kwargs)

class Axe(Weapon):
    _prefix = "axe"

    def __init__(self, **kwargs):
        kwargs['type'] = "axe"
        kwargs['min_factor'] = 0.5
        kwargs['max_factor'] = 2.0
        super(Axe, self).__init__(**kwargs)


class Bow(Weapon):
    _prefix = "bow"

    def __init__(self, **kwargs):
        kwargs['type'] = "bow"
        kwargs['min_factor'] = 0.8
        kwargs['max_factor'] = 1.5
        super(Bow, self).__init__(**kwargs)

class Armor(Gear):
    _prefix = "armor"

    def __init__(self, **kwargs):
        kwargs['slot'] = "armor"
        super(Armor, self).__init__(**kwargs)

        self.toughness = kwargs['toughness']

class Accessory(Gear):
    _prefix = "accessory"

    def __init__(self, **kwargs):
        kwargs['slot'] = "accessory"
        super(Accessory, self).__init__(**kwargs)

# Skills
class Skill(Stuff):
    _prefix = "skill"

    def __init__(self, **kwargs):
        kwargs['category'] = "skill"
        super(Skill, self).__init__(**kwargs)

# Items
class Item(Stuff):
    _prefix = "item"

    def __init__(self, **kwargs):
        kwargs['category'] = "item"
        super(Item, self).__init__(**kwargs)

# Spells
class Spell(Stuff):
    _prefix = "spell"

    def __init__(self, **kwargs):
        kwargs['category'] = "spell"
        super(Spell, self).__init__(**kwargs)


### FUNCTIONS
def load_weapons():
    """ Load all weapon files from disk into cache """
    for entry in os.scandir(os.getenv('DATA_PATH')):
        if entry.is_file():
            # Only grab by weapon type
            if entry.name.split("_")[0] == 'sword':
                new_weapon = Sword.load(entry.name)
            elif entry.name.split("_")[0] == 'axe':
                new_weapon = Axe.load(entry.name)
            elif entry.name.split("_")[0] == 'bow':
                new_weapon = Bow.load(entry.name)
            else:
                continue

            # Append and look for the next one
            WEAPONS.append(new_weapon)
            continue


def load_armor():
    """ Loads armor for sale from disk """
    pass

def load_accessories():
    """ Loads accessories for sale from disk """
    pass

def load_spells():
    """ Loads spells for sale from disk """
    pass

def load_all():
    """ Loads all available items for sale from disk """
    load_weapons()
    load_armor()
    load_accessories()
    load_spells()
