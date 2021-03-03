import os
import shutil
import pytest
from bot.components import users, stuff
from bot.api import shop, errors

@pytest.fixture
def environment():
    """ Configures the environment before and after tests """
    # Change the save path to the /tmp part of the disk to avoid data clobbering
    try:
        shutil.rmtree('/tmp/discord_bot')
    except FileNotFoundError:
        pass
    os.makedirs('/tmp/discord_bot/test')
    os.environ["DATA_PATH"] = '/tmp/discord_bot/test'

    stuff.WEAPONS = [stuff.Sword(name="test sword", desc="You should never see this", power=1, value=10)]
    stuff.ARMOR = [stuff.Armor(name="test armor", desc="You should never see this", toughness=1, value=10)]
    stuff.ACCESSORIES = [stuff.Accessory(name="test accessory", desc="You should never see this", value=10)]
    stuff.ITEMS = [stuff.Item(name="test item", desc="You should never see this", value=10)]
    stuff.SPELLS = [stuff.Spell(name="test spell", desc="You should never see this", value=10)]
    users.create("user")

    yield

    users.CACHE = {}
    stuff.WEAPONS = []
    stuff.ARMOR = []
    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_list(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Test listing out all the items for sale """
    weapons = shop.list_weapons()
    assert len(weapons) == 1
    assert weapons[0] == "test sword"

    armor = shop.list_armor()
    assert len(armor) == 1
    assert armor[0] == "test armor"

    accessories = shop.list_accessories()
    assert len(accessories) == 1
    assert accessories[0] == "test accessory"

    items = shop.list_items()
    assert len(items) == 1
    assert items[0] == "test item"

    spells = shop.list_spells()
    assert len(spells) == 1
    assert spells[0] == "test spell"

    everything = shop.list_all()
    assert everything['weapons'] == weapons
    assert everything['armor'] == armor
    assert everything['accessories'] == accessories
    assert everything['items'] == items
    assert everything['spells'] == spells

#@pytest.mark.skip(reason="implementing")
def test_info(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Listing items """
    info = shop.weapon_info("test sword")
    assert info['name'] == stuff.WEAPONS[0].name
    assert info['desc'] == stuff.WEAPONS[0].desc
    assert info['power'] == stuff.WEAPONS[0].power
    assert info['value'] == stuff.WEAPONS[0].value
    with pytest.raises(errors.CommandError):
        shop.weapon_info("Bad name")

    info = shop.armor_info("test armor")
    assert info['name'] == stuff.ARMOR[0].name
    assert info['desc'] == stuff.ARMOR[0].desc
    assert info['toughness'] == stuff.ARMOR[0].toughness
    assert info['value'] == stuff.ARMOR[0].value
    with pytest.raises(errors.CommandError):
        shop.armor_info("Bad name")

    info = shop.accessory_info("test accessory")
    assert info['name'] == stuff.ACCESSORIES[0].name
    assert info['desc'] == stuff.ACCESSORIES[0].desc
    assert info['value'] == stuff.ACCESSORIES[0].value
    with pytest.raises(errors.CommandError):
        shop.accessory_info("Bad name")

    info = shop.item_info("test item")
    assert info['name'] == stuff.ITEMS[0].name
    assert info['desc'] == stuff.ITEMS[0].desc
    assert info['value'] == stuff.ITEMS[0].value
    with pytest.raises(errors.CommandError):
        shop.item_info("Bad name")

    info = shop.spell_info("test spell")
    assert info['name'] == stuff.SPELLS[0].name
    assert info['desc'] == stuff.SPELLS[0].desc
    assert info['value'] == stuff.SPELLS[0].value
    with pytest.raises(errors.CommandError):
        shop.spell_info("Bad name")

#@pytest.mark.skip(reason="implementing")
def test_buy_sell(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Test buying and selling stuff """
    # Buy 2 of the same item
    user = users.CACHE['user']
    test_gold = stuff.WEAPONS[0].value
    user.earn(test_gold * 2)

    shop.buy(user.name, stuff.WEAPONS[0].name)
    assert user.gold == test_gold
    assert len(user.inventory) == 1
    assert user.inventory[0]['item'].name == stuff.WEAPONS[0].name
    assert user.inventory[0]['quantity'] == 1

    shop.buy(user.name, stuff.WEAPONS[0].name)
    assert user.gold == 0
    assert len(user.inventory) == 1
    assert user.inventory[0]['item'].name == stuff.WEAPONS[0].name
    assert user.inventory[0]['quantity'] == 2

    # Sell one at a time
    shop.sell(user.name, stuff.WEAPONS[0].name)
    assert user.gold == test_gold
    assert len(user.inventory) == 1
    assert user.inventory[0]['quantity'] == 1

    shop.sell(user.name, stuff.WEAPONS[0].name)
    assert user.gold == test_gold * 2
    assert len(user.inventory) == 0

    # Buy something you can't afford or something that doesn't exist
    user._gold = 0
    with pytest.raises(errors.CommandError):
        shop.buy(user.name, stuff.WEAPONS[0].name)
    with pytest.raises(errors.CommandError):
        shop.buy("foobar", stuff.WEAPONS[0].name)
    with pytest.raises(errors.CommandError):
        shop.buy(user.name, "foobar")
