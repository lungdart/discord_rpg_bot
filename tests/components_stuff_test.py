import os
import shutil
import pytest
from bot.components import stuff

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

    stuff.WEAPONS = {}
    stuff.ARMOR = {}
    stuff.ACCESSORIES = {}
    stuff.ITEMS = {}
    stuff.SKILLS = {}
    stuff.SPELLS = {}
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
    assert weapon.type == "sword"

    weapon.save()
    weapon2 = stuff.Sword.load(name)
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
    assert weapon.type == "axe"

    weapon.save()
    weapon2 = stuff.Axe.load(name)
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
    assert weapon.type == "bow"

    weapon.save()
    weapon2 = stuff.Bow.load(name)
    assert weapon.__dict__ == weapon2.__dict__

#@pytest.mark.skip(reason="implementing")
def test_all_weapons(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test all three weapon types """
    # Save out 9 weapons
    weapons = [
        stuff.Sword(name='sword1', desc='A sword', power=1),
        stuff.Axe(name='axe1', desc='An axe', power=2),
        stuff.Bow(name='bow1', desc='A Bow', power=3),

        stuff.Sword(name='sword2', desc='Another sword', power=4),
        stuff.Axe(name='axe2', desc='Another axe', power=5),
        stuff.Bow(name='bow2', desc='Another Bow', power=6),

        stuff.Sword(name='sword3', desc='Yet another sword', power=7),
        stuff.Axe(name='axe3', desc='Yet another axe', power=8),
        stuff.Bow(name='bow3', desc='Yet another Bow', power=9)
    ]
    for entry in weapons:
        entry.save

    # Load them back in
    stuff.load_weapons()
    assert len(stuff.WEAPONS) == 9

    swords = 0
    axes = 0
    bows = 0
    for entry in stuff.WEAPONS:
        if entry.type == 'sword':
            sword += 1
        elif entry.type == 'axe':
            axe += 1
        elif entry.type == 'bow':
            bow += 1
    assert swords == 3
    assert axes == 3
    assert bows == 3


@pytest.mark.skip(reason="implementing")
def test_armor(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test armors """
    pass

@pytest.mark.skip(reason="implementing")
def test_accessory(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test accessories """
    pass

@pytest.mark.skip(reason="implementing")
def test_skill(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test skills """
    pass

@pytest.mark.skip(reason="implementing")
def test_item(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test items """
    pass

@pytest.mark.skip(reason="implementing")
def test_spell(environment): # pylint: disable=redefined-outer-name,unused-argument
    """ Create, save and load test spells """
    pass
