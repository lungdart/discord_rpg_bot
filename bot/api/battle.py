""" User level battle commands """
from bot.api.errors import CommandError
from bot.components import users

def join(username):
    """ Joins a user to a waiting battle """
    pass

def attack(username, target):
    """ Attack a target """
    pass

def defend(username):
    """ Defend for the turn """
    pass

def use(username, target, skill, **kwargs):
    """ Use a skill on a target """
    pass
