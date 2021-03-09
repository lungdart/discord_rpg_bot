import os
import shutil
import pytest
from bot.components import stuff
from bot.api import shop

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

    shop.WEAPONS = []
    shop.ARMOR = []
    shop.ACCESSORIES = []
    shop.ITEMS = []
    shop.SPELLS = []
    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_sword(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test swords """
    name = "sword1"
    desc = "A sword"
    power = 10
    weapon = stuff.Sword(name=name, desc=desc, power=power)

    assert weapon.name == name
    assert weapon.desc == desc
    assert weapon.power == power
    assert weapon.category == "gear"
    assert weapon.slot == "weapon"
    assert weapon.type == "sword"

    filename = os.path.join(os.getenv('DATA_PATH'), 'test_sword.json')
    weapon.save(filename)
    weapon2 = stuff.Sword.load(filename)
    assert weapon.__dict__ == weapon2.__dict__

#@pytest.mark.skip(reason="implementing")
def test_axe(environment):# pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test axes """
    name = "axe1"
    desc = "An axe"
    power = 10
    weapon = stuff.Axe(name=name, desc=desc, power=power)

    assert weapon.name == name
    assert weapon.desc == desc
    assert weapon.power == power
    assert weapon.category == "gear"
    assert weapon.slot == "weapon"
    assert weapon.type == "axe"

    filename = os.path.join(os.getenv('DATA_PATH'), 'test_axe.json')
    weapon.save(filename)
    weapon2 = stuff.Axe.load(filename)
    assert weapon.__dict__ == weapon2.__dict__

#@pytest.mark.skip(reason="implementing")
def test_bow(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test bows """
    name = "bow1"
    desc = "A bow"
    power = 10
    weapon = stuff.Bow(name=name, desc=desc, power=power)

    assert weapon.name == name
    assert weapon.desc == desc
    assert weapon.power == power
    assert weapon.category == "gear"
    assert weapon.slot == "weapon"
    assert weapon.type == "bow"

    filename = os.path.join(os.getenv('DATA_PATH'), 'test_bow.json')
    weapon.save(filename)
    weapon2 = stuff.Bow.load(filename)
    assert weapon.__dict__ == weapon2.__dict__


#@pytest.mark.skip(reason="implementing")
def test_armor(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test armors """
    name = "armor1"
    desc = "Some armor"
    toughness = 10
    armor = stuff.Armor(name=name, desc=desc, toughness=toughness)

    assert armor.name == name
    assert armor.desc == desc
    assert armor.toughness == toughness
    assert armor.category == "gear"
    assert armor.slot == "armor"

    filename = os.path.join(os.getenv('DATA_PATH'), 'test_armor.json')
    armor.save(filename)
    armor2 = stuff.Armor.load(filename)
    assert armor.__dict__ == armor2.__dict__

@pytest.mark.skip(reason="implementing")
def test_accessory(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test accessories """
    pass

@pytest.mark.skip(reason="implementing")
def test_item(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test items """
    pass

@pytest.mark.skip(reason="implementing")
def test_spell(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test spells """
    pass
