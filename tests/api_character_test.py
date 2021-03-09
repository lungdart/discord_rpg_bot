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

        def __init__(self):
            self.logger = logging.NullLogger()
            self.api = bot.api.API(self.logger)
            self.api.character.create("User")

    yield Fixture()

    shutil.rmtree('/tmp/discord_bot')

#@pytest.mark.skip(reason="implementing")
def test_stats(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the stats command """
    # Test getting stats for a bad user
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.stats("foobar")

    user = env.api.character.get('UsEr')
    stats = env.api.character.stats('UsEr')
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
def test_equip(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests equipping """

    # User should be empty to start, with equipment in inventory
    user = env.api.character.get('UsEr')
    user.give(env.weapon)
    user.give(env.armor)
    user.give(env.accessory)
    stats = env.api.character.stats('UsEr')
    assert len(stats['inventory']) == 3
    assert stats['weapon'] == 'Empty'
    assert stats['armor'] == 'Empty'
    assert stats['accessory'] == 'Empty'

    # Test edge cases
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.equip("foobar", env.weapon.name)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.equip('UsEr', 'foobar')

    # Actually equip the gear and ensure it modifies the character correctly, and comes out of inventory
    env.api.character.equip('UsEr', env.weapon.name)
    env.api.character.equip('UsEr', env.armor.name)
    env.api.character.equip('UsEr', env.accessory.name)
    stats = env.api.character.stats('UsEr')
    assert len(stats['inventory']) == 0
    assert stats['weapon'] == env.weapon.name
    assert stats['armor'] == env.armor.name
    assert stats['accessory'] == env.accessory.name
    assert stats['power'] == env.weapon.power
    assert stats['toughness'] == env.armor.toughness

#@pytest.mark.skip(reason="implementing")
def test_unequip(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests unequipping works correctly """
    user = env.api.character.get('UsEr')
    user.give(env.weapon)
    user.give(env.armor)
    user.give(env.accessory)
    env.api.character.equip('UsEr', env.weapon.name)
    env.api.character.equip('UsEr', env.armor.name)
    env.api.character.equip('UsEr', env.accessory.name)

    # Test getting stats for a bad user
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.unequip("foobar", "weapon")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.unequip('UsEr', 'foobar')

    # Actually unequip and ensure everythings back to normal
    env.api.character.unequip('UsEr', "weapon")
    env.api.character.unequip('UsEr', "armor")
    env.api.character.unequip('UsEr', "accessory")

    stats = env.api.character.stats('UsEr')
    assert len(stats['inventory']) == 3
    assert stats['weapon'] == 'Empty'
    assert stats['armor'] == 'Empty'
    assert stats['accessory'] == 'Empty'
    assert stats['power'] == 1
    assert stats['toughness'] == 1
