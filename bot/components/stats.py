""" Stat objects make life a little easier """

class CoreStat():
    """ Core stats are what go up and down to modify the character """
    def __init__(self, base_value, current_value=None):
        self._base = base_value
        self.current = current_value if current_value else self.base

    @property
    def base(self):
        """ Prevents base from being modified accidentally """
        return self._base

    def restore(self):
        """ Restores the current value back to baseline """
        self.current = self._base

    def modify(self, amount):
        """ Modifies the base value by the given amount """
        self._base += amount
        self.restore()

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

    def restore(self):
        """ Restores the current value back to the given amount """
        self.current = self.base
