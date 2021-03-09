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

    stuff.WEAPONS = []
    stuff.ARMOR = []
    stuff.ACCESSORIES = []
    stuff.ITEMS = []
    stuff.SPELLS = []
    shutil.rmtree('/tmp/discord_bot')


#@pytest.mark.skip(reason="implementing")
def test_factory(): # pylint: disable=redefined-outer-name,unused-argument
    """ Test creating items from the factory method """
    sword1 = stuff.Sword(name="test", desc="test2", power=42)
    sword2 = stuff.factory(**sword1.__dict__)
    assert sword1 == sword2

    axe1 = stuff.Axe(name="test", desc="test2", power=42)
    axe2 = stuff.factory(**axe1.__dict__)
    assert axe1 == axe2

    bow1 = stuff.Bow(name="test", desc="test2", power=42)
    bow2 = stuff.factory(**bow1.__dict__)
    assert bow1 == bow2

    armor1 = stuff.Armor(name="test", desc="test2", toughness=42)
    armor2 = stuff.factory(**armor1.__dict__)
    assert armor1 == armor2

    accessory1 = stuff.Accessory(name="test", desc="test2")
    accessory2 = stuff.factory(**accessory1.__dict__)
    assert accessory1 == accessory2

    spell1 = stuff.Spell(name="test", desc="test2")
    spell2 = stuff.factory(**spell1.__dict__)
    assert spell1 == spell2

    item1 = stuff.Item(name="test", desc="test2")
    item2 = stuff.factory(**item1.__dict__)
    assert item1 == item2


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
    assert weapon.slot == "weapon"
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
    assert weapon.slot == "weapon"
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
        entry.save()

    # Load them back in
    stuff.load_weapons()
    assert len(stuff.WEAPONS) == 9

    swords = 0
    axes = 0
    bows = 0
    for entry in stuff.WEAPONS:
        if entry.type == 'sword':
            swords += 1
        elif entry.type == 'axe':
            axes += 1
        elif entry.type == 'bow':
            bows += 1
    assert swords == 3
    assert axes == 3
    assert bows == 3


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

    armor.save()
    armor2 = stuff.Armor.load(name)
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
