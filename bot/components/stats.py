""" Stat objects make life a little easier """

class CoreStat():
    """ Core stats are what go up and down to modify the character """
    def __init__(self, base_value, current_value=None):
        self._base = base_value
        self._current = current_value if current_value else self.base

    @property
    def base(self):
        """ Force use of setter/getter """
        return self._base

    @base.setter
    def base(self, value):
        """ Sets the base and current stat at the same time without going below 1 """
        self._base = value
        if self._base < 1:
            self._base = 1

        self.restore()

    @property
    def current(self):
        """ current getter """
        return self._current

    @current.setter
    def current(self, value):
        """ current setter """
        self._current = value
        if self._current < 0:
            self._current = 0

    def restore(self):
        """ Restores the current value back to baseline """
        self.current = self._base

    def __getstate__(self):
        """ Serialize core stat """
        return {"base": self._base}

    def __setstate__(self, state):
        """ Deserialize core stat """
        self._base = state["base"]
        self.current = self._base

class DerivedStat():
    """ Derived stats are based off core stats, and change when their core changes """
    def __init__(self, core_stat, factor=1.0, offset=0):
        self.core_stat = core_stat
        self.factor = factor
        self.offset = offset
        self._current = self.base

    @property
    def base(self):
        """ Programmatically calculates the base value """
        return (self.core_stat.current * self.factor) + self.offset

    @property
    def current(self):
        """ Update than grab the current value """
        # In the event of a debuf to the core stat, cut off the current value.
        if self._current > self.base:
            self._current = self.base
        return self._current

    @current.setter
    def current(self, value):
        """ Sets the current value """
        self._current = value
        if self._current < 0:
            self._current = 0

    def restore(self):
        """ Restores the current value back to the given amount """
        self._current = self.base

    def __getstate__(self):
        """ Serialize derived stat """
        # The core stats are saved under the derived stats for easier serializing
        return {
            "core_stat": self.core_stat.__getstate__(),
            "factor": self.factor,
            "offset": self.offset
        }

    def __setstate__(self, state):
        """ Deserialize derived stat """
        # Deserialize the corestat reference first
        core_stat = CoreStat(1)
        core_stat.__setstate__(state['core_stat'])

        self.core_stat = core_stat
        self.factor = state['factor']
        self.offset = state['offset']
        self._current = self.base
