import pytest
from bot.components import stats

#@pytest.mark.skip(reason="implementing")
def test_squish():
    """ Test creating core and derived stats """
    old_stat = stats.CoreStat()
    points = 4
    factor = 20
    offset = 69
    old_stat.set_derived(factor, offset)
    old_stat.upgrade(points)

    squished = old_stat.__getstate__()
    assert squished['points'] == points
    assert squished['derived_factor'] == factor
    assert squished['derived_offset'] == offset

    new_stat = stats.CoreStat()
    new_stat.__setstate__(squished)

    assert new_stat.base == old_stat.base
    assert new_stat.current == old_stat.base
    assert new_stat.derived.factor == old_stat.derived.factor
    assert new_stat.derived.offset == old_stat.derived.offset
    assert new_stat.derived.base == old_stat.derived.base
    assert new_stat.derived.current == old_stat.derived.base

#@pytest.mark.skip(reason="implementing")
def test_core_modify():
    """ Test restoring a core stat """
    core_stat = stats.CoreStat()

    # Verify upgrading the core stat works
    points = 9
    core_stat.upgrade(points)
    assert core_stat.base == 1 + points
    assert core_stat.base == core_stat.current

    # Verify hurting and restorying the current value works
    core_stat.current = -99
    assert core_stat.current == 0
    core_stat.restore()
    assert core_stat.base == core_stat.current

    # Verify the upgrade tool can't be misused
    core_stat.upgrade(0) # Will force upgrading of 1
    assert core_stat.current == core_stat.base
    assert core_stat.base == 1 + points + 1

    core_stat.upgrade(-99) # Will force upgrading of 1
    assert core_stat.current == core_stat.base
    assert core_stat.base == 1 + points + 2

    # Verify restarting the stat works
    value = core_stat.restart()
    assert value == points + 2
    assert core_stat.current == core_stat.base
    assert core_stat.base == 1

def test_derived_modify():
    """ Test restoring a derived stat """
    # Verify the derived stat derives value from the core stat
    core_stat = stats.CoreStat()
    derived_stat = core_stat.derived
    assert derived_stat.base == 1
    assert derived_stat.base == derived_stat.current

    # Ensure bad values dont work
    derived_stat.current = -99
    assert derived_stat.current == 0

    # Ensure upgrading the core stat is reflected in the derived stat
    points = 9
    core_stat.upgrade(points)
    assert derived_stat.current == derived_stat.base
    assert derived_stat.base == 1 + points
