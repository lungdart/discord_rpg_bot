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

    class FakeContext():
        channel = None
        author = None

    class Fixture():
        ctx = FakeContext()
        weapon = stuff.Sword(name="test sword", desc="You should never see this", power=1, value=10)
        armor = stuff.Armor(name="test armor", desc="You should never see this", toughness=1, value=10)
        accessory = stuff.Accessory(name="test accessory", desc="You should never see this", value=10)

        def __init__(self):
            self.api = bot.api.API()
            self.api.character.create("User")

    yield Fixture()

    shutil.rmtree('/tmp/discord_bot')

#@pytest.mark.skip(reason="implementing")
def test_create(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests loading all characters from disk """
    # Ensure the api can create characters
    env.api.character.create('test')
    env.api.character.create_missing(['user1', 'user2', 'user3'])
    assert len(env.api.character.cache) == 5

    # Ensure the api skips over creating existing characters
    env.api.character.create_missing(['test', 'user', 'user1', 'user2', 'user3'])
    assert len(env.api.character.cache) == 5

    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.create('user') # Should already exist

#@pytest.mark.skip(reason="implementing")
def test_load_unload(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests loading all characters from disk """
    # Ensure that loading and unloading passes uninteresting files
    with open('/tmp/discord_bot/test/foobar.null', 'w') as filename:
        filename.write("Hello world")

    # Create then unload the users
    env.api.character.create_missing(['user', 'user1', 'user2', 'user3'])
    env.api.character.unload('user1')
    env.api.character.unload('user2')
    env.api.character.unload('user3')
    assert len(env.api.character.cache) == 1 # there's already a user in cache

    # Load them all back in
    env.api.character.load_all()
    assert len(env.api.character.cache) == 4 # The 3 new characters + the 1 preexisting one
    assert 'user1' in env.api.character.cache
    assert 'user2' in env.api.character.cache
    assert 'user3' in env.api.character.cache

    # Unload everything and then load one by one
    env.api.character.unload('user1')
    env.api.character.load('user1')
    assert 'user1' in env.api.character.cache

#@pytest.mark.skip(reason="implementing")
def test_stats(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the stats command """
    # Test getting stats for a bad user
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.stats("foobar")

    user = env.api.character.get('UsEr')
    user._gold = 0 # Remove debugging initial gold values
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

#@pytest.mark.skip(reason="implementing")
def test_give_gold(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests giving gold to a character """
    # Reset the users gold to 0 incase there's a starting amount for debugging
    user = env.api.character.get('UsEr')
    user._gold = 0

    # Give a character gold
    gold = 420
    env.api.character.give_gold('uSeR', gold)
    assert user._gold == gold

    # Give a character a bad amount of gold
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.give_gold('user', -1)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.give_gold('user', "foobar")

#@pytest.mark.skip(reason="implementing")
def test_give_xp(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests giving gold to a character """
    user = env.api.character.get('UsEr')

    # Give a character gold
    base_xp = 10
    env.api.character.give_xp(env.ctx, 'uSeR', base_xp)
    assert user.experience == base_xp
    assert user.level == 1
    assert user.points == 0

    # Give character enough experience to force a few level ups
    additional_xp = 6000
    env.api.character.give_xp(env.ctx, 'UsEr', additional_xp)
    assert user.experience == base_xp
    assert user.level == 7
    assert user.points == 30

    # Give a character a bad amount of gold
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.give_xp(env.ctx, 'user', -1)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.give_xp(env.ctx, 'user', "foobar")

#@pytest.mark.skip(reason="implementing")
def test_spend_points(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests spending skill points """
    user = env.api.character.get('uSeR')

    # Give character enough experience to force a few level ups and get skill points
    xp = 6000
    env.api.character.give_xp(env.ctx, 'UsEr', xp)
    assert user.points == 30

    # Upgrade each stat once
    env.api.character.spend_points('user', 'body')
    env.api.character.spend_points('user', 'mind')
    env.api.character.spend_points('user', 'agility')
    assert user.points == 27
    assert user.body.base == 2
    assert user.mind.base == 2
    assert user.agility.base == 2
    assert user.life.base == ((2 * 25) + 100)
    assert user.mana.base == ((2 * 5) + 5)
    assert user.speed.base == (2 * 2)

    env.api.character.spend_points('user', 'body', 27)
    assert user.points == 0
    assert user.body.base == 29
    assert user.life.base == ((29 * 25) + 100)

    # try to spend bad points on bad stats
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.spend_points('user', 'body', -1)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.spend_points('user', 'mind', 999999999)
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.spend_points('user', 'body', "foobar")
    with pytest.raises(bot.api.errors.CommandError):
        env.api.character.spend_points('user', 'foobar')

    # Verify restarting points works
    env.api.character.restart_points('user')
    assert user.points == 30
    assert user.body.base == 1
    assert user.mind.base == 1
    assert user.agility.base == 1
    assert user.life.base == 125
    assert user.mana.base == 10
    assert user.speed.base == 2
