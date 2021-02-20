""" User object """
from bot.components.stats import CoreStat, DerivedStat


### GLOBALS
CACHE = {}


### CLASS DEFINITIONS
class User():
    """ User object """
    def __init__(self, name):
        self.name = name
        self.body = None
        self.mind = None
        self.agility = None
        self.life = None
        self.mana = None
        self.speed = None
        self.armor = None
        self.accessory = None
        self.items = []
        self.skills = []

    @classmethod
    def create(cls, name):
        """ Creates a new user with default values """
        this = cls(name)
        this.body = CoreStat(1)
        this.mind = CoreStat(1)
        this.agility = CoreStat(1)

        # Derived stats
        this.life = DerivedStat(this.body, factor=25, offset=100)
        this.mana = DerivedStat(this.mind, factor=5, offset=5)
        this.speed = DerivedStat(this.agility, factor=2, offset=0)

        # Items
        this.armor = None
        this.accessory = None
        this.items = []

        # Skills
        this.skills = []

        return this
    @classmethod
    def load(cls, name):
        """ Load user from disk """
        this = cls(name)
        return this

    def save(self):
        """ Saves this user to disk """

    def restore(self):
        """ Restores this user back to base line """
        self.body.restore()
        self.mind.restore()
        self.agility.restore()

        self.life.restore()
        self.mana.restore()
        self.speed.restore()


### USER FETCHING
def load(name):
    """ Get's the named user instance """
    user = None
    try:
        user = CACHE[name]
    except KeyError:
        user = User.load(name)
        CACHE[name] = user
    except IOError:
        user = User.create(name)
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
