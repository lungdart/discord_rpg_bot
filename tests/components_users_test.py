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

    users.CACHE = {}
    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_user(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save, and load a user """
    name = "Testy123"
    user_1 = users.create(name) # Implicit save call
    user_2 = users.load(name)

    assert user_1 == user_2

    users.unload(name)

    assert not users.CACHE

#@pytest.mark.skip(reason="implementing")
def test_multi_user(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save, and load multiple users """
    assert not users.CACHE

    name_1 = "Testy123"
    name_2 = "Yolo420"
    user_1 = users.create(name_1)
    user_2 = users.create(name_2)
    assert user_1 != user_2

    users.unload(name_1)
    assert len(users.CACHE) == 1

    users.unload(name_2)
    assert not users.CACHE
