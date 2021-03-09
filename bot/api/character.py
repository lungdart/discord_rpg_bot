""" Passive character commands """
import os
from bot.components import users
from bot.api.errors import CommandError

class CharacterAPI():
    """ Character API utilizes caching """

    def __init__(self, parent):
        self._parent = parent

        self.cache = {}
        self.load_all()

    def load_all(self):
        """ Loads all existing users from disk """
        for entry in os.scandir(os.getenv('DATA_PATH')):
            if entry.is_file():
                file_no_ext = os.path.splitext(entry.name)[0]
                parts = file_no_ext.split("_")
                category = parts[0]

                if category == 'user':
                    user = users.User.load(entry.name)
                    lowercase = user.name.lower()
                    self.cache[lowercase] = user
                else:
                    continue

    def create(self, username):
        """ Creates a new user and saves to disk """
        lowercase = username.lower()
        if lowercase in self.cache:
            raise CommandError(f"Can't create {username} character because it already exists")

        user = users.User.create(username)
        self.cache[lowercase] = user
        self.save(username)

        return user

    def save(self, username):
        """ Saves the username to disk """
        user = self.get(username)
        underscored_name = user.name.replace(' ', '_')
        filename = os.path.join(os.getenv('DATA_PATH'), f'user_{underscored_name}.json')
        user.save(filename)

    def get(self, username):
        """ Gets the named user instance prefering cache over disk"""
        lowercase = username.lower()
        try:
            return self.cache[lowercase]
        except KeyError:
            pass

        try:
            return self.load(username)
        except FileNotFoundError:
            raise CommandError(f"Could not find {username} in cache or on disk")

    def load(self, username):
        """ Instantiate the named user instance from disk """
        user = users.User.load(username)

        lowercase = username.lower()
        self.cache[lowercase] = user
        return user

    def unload(self, username):
        """ Save then unload a user from cache """
        # Load and save the user first
        user = self.get(username)
        user.save()

        # Ensure the user is unloaded
        lowercase = username.lower()
        del self.cache[lowercase]

    def stats(self, username):
        """ Get the stats for the target user """
        # User stats are not private information. Anyone can request it
        target = self.get(username)
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
            'inventory'      : [f"{x['item'].name} x{x['quantity']}" for x in target.inventory],
            'gold'           : target.gold
        }

        return result

    def equip(self, username, name):
        """ Equip an item by name"""
        target = self.get(username)

        item = None
        for entry in target.inventory:
            if entry['item'].name == name:
                item = entry['item']
        if item is None:
            raise CommandError(f"Could not find {name} in {target.name}'s inventory")

        if not target.equip(item):
            raise CommandError(f"Could not equip {name}")

        self.save(username)

    def unequip(self, username, slot):
        """ Unequip anything in a slot """
        target = self.get(username)
        if not target.unequip(slot):
            raise CommandError(f"Invalid equipment slot: {slot}")

        self.save(username)
