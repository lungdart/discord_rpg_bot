import os
import json
import random


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
    def load(cls, filename):
        """ Load object from disk """
        with open(filename, 'r') as file:
            data = json.load(file)

        this = cls(**data)
        return this

    def save(self, filename):
        """ Saves this user to disk """
        data = json.dumps(self.__dict__)
        with open(filename, 'w') as file:
            file.write(data)

    def __eq__(self, other):
        """ Test equality by attribute dict """
        return self.__dict__ == other.__dict__


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


def factory(**kwargs):
    """ Creates the appropriate instance from the given dictionary """
    # Weapons
    if kwargs['category'] == "gear":
        if kwargs["slot"] == "weapon":
            if kwargs['type'] == "sword":
                return Sword(**kwargs)
            if kwargs['type'] == "axe":
                return Axe(**kwargs)
            if kwargs['type'] == "bow":
                return Bow(**kwargs)
            raise KeyError("Bad weapon type")

        # Non weapon gear
        if kwargs["slot"] == "armor":
            return Armor(**kwargs)
        if kwargs["slot"] == "accessory":
            return Accessory(**kwargs)
        raise KeyError("Bad equipment slot")

    # Non gear
    if kwargs['category'] == "spell":
        return Spell(**kwargs)
    if kwargs['category'] == "item":
        return Item(**kwargs)

    raise KeyError("Bad category key")
