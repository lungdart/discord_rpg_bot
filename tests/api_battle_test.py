import os
import shutil
import pytest
from bot.components import users, stuff, logger
from bot.api import battle, errors

### FIXTURES ###
@pytest.fixture
def new_battle():
    """ Configures the environment before and after tests """
    # Change the save path to the /tmp part of the disk to avoid data clobbering
    try:
        shutil.rmtree('/tmp/discord_bot')
    except FileNotFoundError:
        pass
    os.makedirs('/tmp/discord_bot/test')
    os.environ["DATA_PATH"] = '/tmp/discord_bot/test'

    # Create some users to battle with, and equip one with stuff
    users.create("user1")
    winner = users.create("user2")
    winner.give(stuff.Sword(name="test sword", desc="You should never see this", power=25, value=10))
    winner.give(stuff.Armor(name="test armor", desc="You should never see this", toughness=25, value=10))
    winner.equip('test sword')
    winner.equip('test armor')

    instance = battle.Battle(logger.NullLogger)

    yield instance

    users.CACHE = {}
    stuff.WEAPONS = []
    stuff.ARMOR = []
    shutil.rmtree('/tmp/discord_bot')


### TESTS ###
#@pytest.mark.skip(reason="implementing")
def test_start_join_stop(new_battle): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the start join and stop battle sequences """
    assert new_battle.is_stopped

    new_battle.new()
    assert new_battle.is_joinable

    user1 = users.load('user1')
    user2 = users.load('user2')
    new_battle.join('user1')
    new_battle.join('user2')
    assert len(new_battle.participants) == 2

    new_battle.start()
    assert new_battle.is_round_wait

    new_battle.stop()
    assert new_battle.is_stopped

#@pytest.mark.skip(reason="implementing")
def test_attack_defend(new_battle): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the attacking and defending commands in battle """
    new_battle.new()

    user1 = users.load('user1')
    user2 = users.load('user2')
    new_battle.join('user1')
    new_battle.join('user2')
    new_battle.start()

    # First command
    assert new_battle.is_round_wait
    new_battle.submit_action('user1', 'attack', target="user2")

    # Last command
    assert new_battle.is_round_wait
    new_battle.submit_action('user2', 'defend')

    # This should be a new round, with damage to user2
    assert new_battle.is_round_wait
    assert user1.life.current == user1.life.base
    assert user2.life.current < user2.life.base

    new_battle.submit_action('user1', 'defend')
    new_battle.submit_action('user2', 'attack', target='user1')
    assert user1.life.current == user1.life.base

    new_battle.stop()
