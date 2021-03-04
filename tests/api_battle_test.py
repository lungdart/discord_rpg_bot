import os
import shutil
import pytest
from bot.components import users, stuff, logger
from bot.api import battle, errors

class FakeLogger():
    def add(self, name, value, inline=False):
        pass

    def send(self):
        pass

    def pm(self, username):
        pass

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

    logger_factory = logger.LoggerFactory(None, FakeLogger())
    instance = battle.Battle(logger_factory)

    yield instance

    users.CACHE = {}
    stuff.WEAPONS = []
    stuff.ARMOR = []
    shutil.rmtree('/tmp/discord_bot')

#@pytest.mark.skip(reason="implementing")
def test_start_join_stop(new_battle): # pylint: disable=redefined-outer-name,unused-argument
    assert new_battle.state == "stopped"

    new_battle.start()
    assert new_battle.state == "joinable"

    user1 = users.load('user1')
    user2 = users.load('user2')
    new_battle.join('user1')
    new_battle.join('user2')
    assert len(new_battle.users) == 2

    new_battle.begin()
    assert new_battle.state == "active"

    new_battle.stop()
    assert new_battle.state == "stopped"
