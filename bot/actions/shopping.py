from bot.components.users import load as load_user
from discord import Embed

def view_shop():
    """ Get stats """
    result = Embed(title=f"Welcome to the shop!", color=0x00ff00)
    result.add_field(name="Weapons", value=f'Sword\nDagger\nAxe\nBow', inline=False)
    result.add_field(name="Armor", value=f'A trusty item!', inline=False)
    result.add_field(name="Accessories", value=f'A trust item!', inline=False)
    result.add_field(name="Skills", value=f'A trust item!', inline=False)
    result.add_field(name="Items", value=f'A trust item!', inline=False)
    result.add_field(name="Spells", value=f'A trust item!', inline=False)

    return result
