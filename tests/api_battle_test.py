import os
import shutil
import pytest
from bot.components import stuff, logging
import bot.api

### FIXTURES ###
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
        weapon = stuff.Sword(name="test sword", desc="You should never see this", power=25, value=10)
        armor = stuff.Armor(name="test armor", desc="You should never see this", toughness=25, value=10)

        def __init__(self):
            self.api = bot.api.API(logging.NullLogger())
            self.api.character.create("User1")
            self.api.character.create("User2")

            # Configure the winning user with test gear
            winner = self.api.character.get('user1')
            winner.give(self.weapon)
            winner.give(self.armor)
            winner.equip('test sword')
            winner.equip('test armor')

    yield Fixture()

    shutil.rmtree('/tmp/discord_bot')


### TESTS ###
#@pytest.mark.skip(reason="implementing")
def test_start_join_stop(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the start join and stop battle sequences """
    assert env.api.battle.is_stopped

    env.api.battle.new()
    assert env.api.battle.is_joinable

    user1 = env.api.character.get('user1')
    user2 = env.api.character.get('user2')
    env.api.battle.join(user1)
    env.api.battle.join(user2)
    assert len(env.api.battle.participants) == 2

    # Shouldn't be able to join twice
    env.api.battle.join(user1)
    assert len(env.api.battle.participants) == 2

    env.api.battle.start()
    assert env.api.battle.is_round_wait

    env.api.battle.stop()
    assert env.api.battle.is_stopped

#@pytest.mark.skip(reason="implementing")
def test_attack_defend(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Tests the attacking and defending commands in battle """
    env.api.battle.new()

    user1 = env.api.character.get('user1')
    user2 = env.api.character.get('user2')
    env.api.battle.join(user1)
    env.api.battle.join(user2)
    env.api.battle.start()

    # First command
    assert env.api.battle.is_round_wait
    env.api.battle.submit_action(user1, 'attack', target=user2)

    # Last command
    assert env.api.battle.is_round_wait
    env.api.battle.submit_action(user2, 'defend')

    # This should be a new round, with damage to user2
    assert env.api.battle.is_round_wait
    assert user1.life.current == user1.life.base
    assert user2.life.current < user2.life.base

    env.api.battle.submit_action(user1, 'defend')
    env.api.battle.submit_action(user2, 'attack', target=user1)
    assert user1.life.current == user1.life.base

    env.api.battle.stop()
