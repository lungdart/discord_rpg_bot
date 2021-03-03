import pytest
from bot.components import stats

#@pytest.mark.skip(reason="implementing")
def test_squish():
    """ Test creating core and derived stats """
    core_stat = stats.CoreStat(42)
    derived_stat = stats.DerivedStat(core_stat, factor=10, offset=69)

    squished = derived_stat.__getstate__()
    assert squished['factor'] == derived_stat.factor
    assert squished['offset'] == derived_stat.offset
    assert squished['core_stat']['base'] == core_stat.base

    derived_stat.__setstate__(squished)
    core_stat = derived_stat.core_stat

    assert core_stat.base == squished['core_stat']['base']
    assert core_stat.current == squished['core_stat']['base']
    assert derived_stat.factor == squished['factor']
    assert derived_stat.offset == squished['offset']

#@pytest.mark.skip(reason="implementing")
def test_core_modify():
    """ Test restoring a core stat """
    base_value = 10
    core_stat = stats.CoreStat(base_value=base_value)
    assert core_stat.base == base_value
    assert core_stat.base == core_stat.current

    core_stat.current = -99
    assert core_stat.current == 0

    core_stat.restore()
    assert core_stat.base == core_stat.current

    base_value = 99
    core_stat.base = base_value
    assert core_stat.current == base_value
    assert core_stat.base == core_stat.current

    # Base stats can't go below 1
    core_stat.base = -99
    assert core_stat.current == 1
    assert core_stat.base == core_stat.current

def test_derived_modify():
    """ Test restoring a derived stat """
    base_value = 10
    core_stat = stats.CoreStat(base_value=base_value)
    derived_stat = stats.DerivedStat(core_stat, factor=1, offset=0)
    assert derived_stat.base == base_value
    assert derived_stat.base == derived_stat.current

    derived_stat.current = -99
    assert derived_stat.current == 0

    base_value = 99
    core_stat.base = base_value
    assert core_stat.base == derived_stat.base

    # Base stats can't go below 1
    core_stat.base = -99
    derived_stat.restore()
    assert derived_stat.base == 1
    assert derived_stat.current == 1
