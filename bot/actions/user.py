from bot.components.users import load as load_user
from discord import Embed

def create_user(username):
    """ Create a new user for the game """

def delete_user(username):
    """ Delete an existing user for the game """

def get_stats(username):
    """ Get stats """
    user = load_user(username)

    result = Embed(title=f"{username}'s stats", color=0x00ff00)
    result.add_field(name="life", value=f'{user.life.current} / {user.life.base}', inline=True)
    result.add_field(name="mana", value=f'{user.mana.current} / {user.mana.base}', inline=True)
    result.add_field(name="speed", value=f'{user.speed.current} / {user.speed.base}', inline=True)
    result.add_field(name="body", value=f'{user.body.current} / {user.body.base}', inline=True)
    result.add_field(name="mind", value=f'{user.mind.current} / {user.mind.base}', inline=True)
    result.add_field(name="agility", value=f'{user.agility.current} / {user.agility.base}', inline=True)

    return result
