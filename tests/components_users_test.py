""" Tests the users components """
import os
import shutil
import pytest
from bot.components import users

@pytest.fixture
def environment():
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
def test_user(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save, and load a user """
    name_1 = "Testy123"
    name_2 = "Yolo420"
    user_1 = users.User.create(name_1)
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
