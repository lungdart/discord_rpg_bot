import random


### GLOBAS
WEAPONS = []
ARMOR = []
ACCESSORIES = []
ITEMS = []
SKILLS = []


### CLASSES
# Base class just in case
class Stuff():
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

# Weapons
class Weapons(Stuff):
    def __init__(self, name, desc, power, min_factor, max_factor):
        super(Weapons, self).__init__(name, desc)
        self.power = power
        self.min_factor = min_factor
        self.max_factor = max_factor

    def calc_power(self):
        """ Calculates the random weapon power fluctuation """
        low = int(self.power * self.min_factor)
        high = int(self.power * self.max_factor)
        power = random.randint(low, high)

        return power

class Sword(Weapon):
    def __init__(self, name, desc, power):
        super(Sword, self).__init__(name, desc, power, 0.8, 1.0)

class Axe(Weapon):
    def __init__(self, name, desc, power):
        super(Sword, self).__init__(name, desc, power, 0.5, 2.0)

class Bow(Weapon):
    def __init__(self, name, desc, power):
        super(Sword, self).__init__(name, desc, power, 0.8, 1.5)

# Armors
class Armor(Stuff):
    def __init__(self, name, desc, toughness):
        super(Armor, self).__init__(name, desc)
        self.toughness = toughness

# Accessories
class Accessory(Stuff):
    def __init__(self, name, desc):
        super(Accessory, self).__init__(name, desc)

# Skills
class Skill(Stuff):
    def __init__(self, name, desc):
        super(Skill, self).__init__(name, desc)

# Items
class Item(Stuff):
    def __init__(self, name, desc):
        super(Item, self).__init__(name, desc)

# Spells
class Spell(Stuff):
    def __init__(self, name, desc):
        super(Spell, self).__init__(name, desc)


### FUNCTIONS
def load_weapons():
    pass

def load_armor():
    pass

def load_accessories():
    pass

def
