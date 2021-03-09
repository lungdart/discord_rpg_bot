import os
import shutil
import pytest
from bot.components import users, stuff
from bot.api import character, errors

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
    users.create("user")

    yield

    users.CACHE = {}
    stuff.WEAPONS = []
    stuff.ARMOR = []
    shutil.rmtree('/tmp/discord_bot')

#@pytest.mark.skip(reason="implementing")
def test_stats(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the stats command """
    user = users.load('user')
    stats = character.stats('user')

    assert stats['username'] == user.name
    assert stats['level'] == user.level
    assert stats['experience'] == user.experience
    assert stats['base_life'] == user.life.base
    assert stats['current_life'] == user.life.current
    assert stats['base_mana'] == user.mana.base
    assert stats['current_mana'] == user.mana.current
    assert stats['base_speed'] == user.speed.base
    assert stats['current_speed'] == user.speed.current
    assert stats['base_body'] == user.body.base
    assert stats['current_body'] == user.body.current
    assert stats['base_mind'] == user.mind.base
    assert stats['current_mind'] == user.mind.current
    assert stats['base_agility'] == user.agility.base
    assert stats['current_agility'] == user.agility.current
    assert stats['weapon'] == 'Empty'
    assert stats['armor'] == 'Empty'
    assert stats['accessory'] == 'Empty'
    assert stats['power'] == 1
    assert stats['toughness'] == 1
    assert stats['gold'] == 0
    assert len(stats['spells']) == 0
    assert len(stats['inventory']) == 0

#@pytest.mark.skip(reason="implementing")
def test_equip(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests equipping """
    # User should be empty to start, with equipment in inventory
    user = users.load('user')
    user.give(stuff.WEAPONS[0])
    user.give(stuff.ARMOR[0])
    user.give(stuff.ACCESSORIES[0])
    stats = character.stats('user')
    assert len(stats['inventory']) == 3
    assert stats['weapon'] == 'Empty'
    assert stats['armor'] == 'Empty'
    assert stats['accessory'] == 'Empty'

    # Ensure user can't equip jibberish
    with pytest.raises(errors.CommandError):
        character.equip('user', 'foobar')

    # Actually equip the gear and ensure it modifies the character correctly, and comes out of inventory
    character.equip('user', stuff.WEAPONS[0].name)
    character.equip('user', stuff.ARMOR[0].name)
    character.equip('user', stuff.ACCESSORIES[0].name)
    stats = character.stats('user')
    assert len(stats['inventory']) == 0
    assert stats['weapon'] == stuff.WEAPONS[0].name
    assert stats['armor'] == stuff.ARMOR[0].name
    assert stats['accessory'] == stuff.ACCESSORIES[0].name
    assert stats['power'] == stuff.WEAPONS[0].power
    assert stats['toughness'] == stuff.ARMOR[0].toughness

#@pytest.mark.skip(reason="implementing")
def test_unequip(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests unequipping works correctly """
    user = users.load('user')
    user.give(stuff.WEAPONS[0])
    user.give(stuff.ARMOR[0])
    user.give(stuff.ACCESSORIES[0])
    character.equip('user', stuff.WEAPONS[0].name)
    character.equip('user', stuff.ARMOR[0].name)
    character.equip('user', stuff.ACCESSORIES[0].name)

    # Ensure you can't just unequip jibberish
    with pytest.raises(errors.CommandError):
        character.unequip('user', 'foobar')

    # Actually unequip and ensure everythings back to normal
    character.unequip('user', "weapon")
    character.unequip('user', "armor")
    character.unequip('user', "accessory")

    stats = character.stats('user')
    assert len(stats['inventory']) == 3
    assert stats['weapon'] == 'Empty'
    assert stats['armor'] == 'Empty'
    assert stats['accessory'] == 'Empty'
    assert stats['power'] == 1
    assert stats['toughness'] == 1
