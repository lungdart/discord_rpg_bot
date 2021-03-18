""" Tests the users components """
import os
import shutil
import pytest
from bot.components import users

@pytest.fixture
def env():
    """ Configures the environment before and after tests """
    # Attempt to remove existing temp path if needed
    try:
        shutil.rmtree('/tmp/discord_bot')
    except FileNotFoundError:
        pass

    os.makedirs('/tmp/discord_bot/test')
    os.environ["DATA_PATH"] = '/tmp/discord_bot/test'

    yield

    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_user(env): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save, and load a user """
    name_1 = "Testy123"
    name_2 = "Yolo420"
    user_1 = users.User.create(name_1)
    user_1._gold = 0 # Reset gold to avoid debugging gold starting values conflicting with tests

    assert user_1.name == "Testy123"
    assert user_1.level == 1
    assert user_1.experience == 0
    assert user_1.body
    assert user_1.mind
    assert user_1.agility
    assert user_1.life
    assert user_1.mana
    assert user_1.speed
    assert user_1.weapon is None
    assert user_1.armor is None
    assert user_1.accessory is None
    assert len(user_1.spells) == 0
    assert len(user_1.inventory) == 0
    assert user_1._gold == 0
    assert not user_1.defending

    # Verify loading a user does not mutate it
    filename = os.path.join(os.getenv('DATA_PATH'), 'test_user.json')
    user_1.save(filename)
    user_1_copy = users.User.load(filename)
    assert user_1.name == user_1_copy.name

def test_level(env):
    """ Test leveling and point usage """
    user = users.User.create("69420")

    # Ensure user doesn't level up until 1000XP is gained
    user.gain_xp(1000)
    user.level_up()

    # User should now have stat points to spend
    assert user.points == 5

    # Spending points should increase stats
    old_body = user.body.base
    old_mind = user.mind.base
    old_agility = user.agility.base
    old_life = user.life.base
    old_mana = user.mana.base
    old_speed = user.speed.base
    user.upgrade('body')
    user.upgrade('mind')
    user.upgrade('agility', 3)
    assert user.points == 0
    assert user.body.base == (old_body + 1)
    assert user.mind.base == (old_mind + 1)
    assert user.agility.base == (old_agility + 3)
    assert user.life.base > old_life
    assert user.mana.base > old_mana
    assert user.speed.base > old_speed

    # Restarting the points goes back to base line
    user.restart()
    assert user.points == 5
    assert user.body.base == old_body
    assert user.mind.base == old_mind
    assert user.agility.base == old_agility
    assert user.life.base == old_life
    assert user.mana.base == old_mana
    assert user.speed.base == old_speed
