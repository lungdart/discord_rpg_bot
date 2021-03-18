""" User object """
import os
import json
from bot.components.stats import CoreStat, DerivedStat
import bot.components.stuff as stuff


### CLASS DEFINITIONS
class User():
    """ User object """
    def __init__(self, name):
        # Meta data
        self.name = name
        self.level = 1
        self.experience = 0
        self.points = 0

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
        self._gold = 100 # Starting gold

        # Battle statuses
        self.defending = False

    @classmethod
    def create(cls, name):
        """ Creates a new user with default values """
        this = cls(name)

        # Core stats
        this.body = CoreStat()
        this.mind = CoreStat()
        this.agility = CoreStat()
        this._derive_stats()

        return this

    @classmethod
    def load(cls, filename):
        """ Load user from disk """
        with open(filename, 'r') as file:
            data = json.load(file)

        this = cls(data["name"])
        this.level = data["level"]
        this.experience = data["experience"]
        this.points = data["points"]

        this.body = CoreStat(data["body_points"])
        this.mind = CoreStat(data["mind_points"])
        this.agility = CoreStat(data["agility_points"])
        this._derive_stats()

        this.weapon = stuff.factory(**data["weapon"]) if data.get("weapon") else None
        this.armor = stuff.factory(**data["armor"]) if data.get("armor") else None
        this.accessory = stuff.factory(**data["accessory"]) if data.get("accessory") else None

        for entry in data["inventory"]:
            item = stuff.factory(**entry["item"])
            new_entry = {"item": item, "quantity": entry["quantity"]}
            this.inventory.append(new_entry)
        for kwargs in data["spells"]:
            this.spells.append(stuff.factory(**kwargs))

        this._gold = data["gold"]

        return this

    def save(self, filename):
        """ Saves this user to disk """
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
        if not isinstance(item, stuff.Stuff):
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
        if not isinstance(item, stuff.Gear):
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

    def upgrade(self, stat_name, points=1):
        """ Spend points to upgrade base stats """
        if self.points < points:
            return False

        # Grab the correct stat
        if stat_name == 'body':
            stat = self.body
        elif stat_name == 'mind':
            stat = self.mind
        elif stat_name == 'agility':
            stat = self.agility
        else:
            return False

        # Upgrade that stat
        stat.upgrade(points)
        self.points -= points
        return True

    def restart(self):
        """ Removes all spent stat points and puts them back into the point pool """
        self.points += self.body.restart()
        self.points += self.mind.restart()
        self.points += self.agility.restart()

    def gain_xp(self, experience):
        """ Gives the user experience points """
        # Give the user at least 1 experience
        experience = int(experience)
        if experience < 1:
            experience = 1
        self.experience += experience

    def level_up(self):
        """ Levels the character up """
        if self.experience >= 1000:
            self.level += 1
            self.points += 5
            self.experience -= 1000
            return True

        return False

    def is_alive(self):
        """ Checks if this user is dead or alive """
        return self.life.current > 0

    def _derive_stats(self):
        """ Generates the derived stats from the core stats """
        # set the correct factors and offsets
        self.body.set_derived(25, 100)
        self.mind.set_derived(5, 5)
        self.agility.set_derived(2, 0)

        # Create pointers
        self.life = self.body.derived
        self.mana = self.mind.derived
        self.speed = self.agility.derived


class UserEncoder(json.JSONEncoder):
    """ A custom JSON encoder that understands our user objects """
    def default(self, obj):
        if isinstance(obj, User):
            # Convert the inventory item objects to kwarg values for later construction
            inventory = []
            for entry in obj.inventory:
                new_entry = entry.copy()
                new_entry['item'] = entry['item'].__dict__
                inventory.append(new_entry)

            return {
                'name'           : obj.name,
                'level'          : obj.level,
                'experience'     : obj.experience,
                'points'         : obj.points,
                'body_points'    : obj.body._points,
                'mind_points'    : obj.mind._points,
                'agility_points' : obj.agility._points,
                'weapon'         : obj.weapon.__dict__ if obj.weapon else None,
                'armor'          : obj.armor.__dict__ if obj.armor else None,
                'accessory'      : obj.accessory.__dict__ if obj.accessory else None,
                'spells'         : [x.__dict__ for x in obj.spells],
                'inventory'      : inventory,
                'gold'           : obj.gold
            }

        else:
            return json.JSONEncoder.default(self, obj)
