""" User object """
import os
import json
from bot.components.stats import CoreStat, DerivedStat


### GLOBALS
CACHE = {}


### CLASS DEFINITIONS
class User():
    """ User object """
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.body = None
        self.mind = None
        self.agility = None
        self.life = None
        self.mana = None
        self.speed = None
        self.weapon = None
        self.armor = None
        self.accessory = None
        self.items = []
        self.skills = []
        self.spells = []
        self.gear = []
        self.gold = 0

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
        this.body = CoreStat(data["body"])
        this.mind = CoreStat(data["mind"])
        this.agility = CoreStat(data["agility"])
        this._derive_stats()

        this.armor = data["armor"]
        this.accessory = data["accessory"]
        this.items = data["items"]
        this.skills = data["skills"]

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
                'body'      : obj.body.base,
                'mind'      : obj.mind.base,
                'agility'   : obj.agility.base,
                'armor'     : obj.armor,
                'accessory' : obj.accessory,
                'items'     : obj.items,
                'skills'    : obj.skills
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
