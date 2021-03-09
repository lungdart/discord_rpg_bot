import os
import shutil
import pytest
from bot.components import users, stuff, logging
import bot.api

@pytest.fixture
def env():
    """ Configures the environment before and after tests """
    # Change the save path to the /tmp part of the disk to avoid data clobbering
    try:
        shutil.rmtree('/tmp/discord_bot')
    except FileNotFoundError:
        pass
    os.makedirs('/tmp/discord_bot/test')
    os.environ["DATA_PATH"] = '/tmp/discord_bot/test'

    class Fixture():
        weapon = stuff.Sword(name="test sword", desc="You should never see this", power=1, value=10)
        armor = stuff.Armor(name="test armor", desc="You should never see this", toughness=1, value=10)
        accessory = stuff.Accessory(name="test accessory", desc="You should never see this", value=10)
        item = stuff.Item(name="test item", desc="You should never see this", value=10)
        spell = stuff.Spell(name="test spell", desc="You should never see this", value=10)

        def __init__(self):
            self.api = bot.api.API(logging.NullLogger())
            self.api.character.create("User")

            self.api.shop.create(**self.weapon.__dict__)
            self.api.shop.create(**self.armor.__dict__)
            self.api.shop.create(**self.accessory.__dict__)
            self.api.shop.create(**self.item.__dict__)
            self.api.shop.create(**self.spell.__dict__)

    yield Fixture()

    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_list(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Test listing out all the items for sale """
    weapons = env.api.shop.list_weapons()
    assert len(weapons) == 1
    assert weapons[0] == "test sword"

    armor = env.api.shop.list_armor()
    assert len(armor) == 1
    assert armor[0] == "test armor"

    accessories = env.api.shop.list_accessories()
    assert len(accessories) == 1
    assert accessories[0] == "test accessory"

    items = env.api.shop.list_items()
    assert len(items) == 1
    assert items[0] == "test item"

    spells = env.api.shop.list_spells()
    assert len(spells) == 1
    assert spells[0] == "test spell"

    everything = env.api.shop.list_all()
    assert everything['weapons'] == weapons
    assert everything['armor'] == armor
    assert everything['accessories'] == accessories
    assert everything['items'] == items
    assert everything['spells'] == spells

#@pytest.mark.skip(reason="implementing")
def test_info(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Listing items """
    info = env.api.shop.find_info("test sword")
    assert info['name'] == env.api.shop.weapons[0].name
    assert info['desc'] == env.api.shop.weapons[0].desc
    assert info['power'] == env.api.shop.weapons[0].power
    assert info['value'] == env.api.shop.weapons[0].value

    info = env.api.shop.find_info("test armor")
    assert info['name'] == env.api.shop.armor[0].name
    assert info['desc'] == env.api.shop.armor[0].desc
    assert info['toughness'] == env.api.shop.armor[0].toughness
    assert info['value'] == env.api.shop.armor[0].value

    info = env.api.shop.find_info("test accessory")
    assert info['name'] == env.api.shop.accessories[0].name
    assert info['desc'] == env.api.shop.accessories[0].desc
    assert info['value'] == env.api.shop.accessories[0].value


    info = env.api.shop.find_info("test item")
    assert info['name'] == env.api.shop.items[0].name
    assert info['desc'] == env.api.shop.items[0].desc
    assert info['value'] == env.api.shop.items[0].value

    info = env.api.shop.find_info("test spell")
    assert info['name'] == env.api.shop.spells[0].name
    assert info['desc'] == env.api.shop.spells[0].desc
    assert info['value'] == env.api.shop.spells[0].value

    # Test edge cases
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.find_info("foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.weapon_info("foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.armor_info("foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.accessory_info("foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.item_info("foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.spell_info("foobar")

#@pytest.mark.skip(reason="implementing")
def test_buy_sell(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Test buying and selling stuff """
    user = env.api.character.get('uSeR')
    test_gold = env.api.shop.weapons[0].value
    user.earn(test_gold * 2)

    env.api.shop.buy(user, env.api.shop.weapons[0].name)
    assert user.gold == test_gold
    assert len(user.inventory) == 1
    assert user.inventory[0]['item'].name == env.api.shop.weapons[0].name
    assert user.inventory[0]['quantity'] == 1

    env.api.shop.buy(user, env.api.shop.weapons[0].name)
    assert user.gold == 0
    assert len(user.inventory) == 1
    assert user.inventory[0]['item'].name == env.api.shop.weapons[0].name
    assert user.inventory[0]['quantity'] == 2

    # Sell one at a time
    env.api.shop.sell(user, env.api.shop.weapons[0].name)
    assert user.gold == test_gold
    assert len(user.inventory) == 1
    assert user.inventory[0]['quantity'] == 1

    env.api.shop.sell(user, env.api.shop.weapons[0].name)
    assert user.gold == test_gold * 2
    assert len(user.inventory) == 0

    # Buying and selling other things
    user._gold = 9999999
    env.api.shop.buy(user, env.api.shop.armor[0].name)
    env.api.shop.buy(user, env.api.shop.accessories[0].name)
    assert len(user.inventory) == 2

    env.api.shop.sell(user, env.api.shop.armor[0].name)
    env.api.shop.sell(user, env.api.shop.accessories[0].name)
    assert len(user.inventory) == 0

    # Test buying edge cases
    user._gold = 0
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.buy(user, env.api.shop.weapons[0].name)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.buy(user, "foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.buy(user, "foobar", -99)

    # Test selling edge cases
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.sell(user, env.api.shop.weapons[0].name)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.sell(user, "foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.shop.sell(user, "foobar", -99)
