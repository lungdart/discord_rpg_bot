""" Stat objects make life a little easier """

class CoreStat():
    """ Core stats are what go up and down to modify the character """
    def __init__(self, points=0):
        points = int(points)
        if points < 0:
            points = 0

        self._points = points
        self._current = self.base
        self._derived = DerivedStat(self.base)

    @property
    def base(self):
        """ Force use of setter/getter """
        return self._points + 1

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

    @property
    def derived(self):
        """ Grab the derived stat """
        return self._derived

    def set_derived(self, factor, offset):
        """ Set's the multiplication factor for the derived stat """
        self.derived._base = self.base
        new_factor = self._derived.factor = factor
        new_offset = self._derived.offset = offset
        self.derived.restore()

        return new_factor, new_offset

    def upgrade(self, points=1):
        """ Increases the core stat by upgrading it """
        points = int(points)
        if points < 1:
            points = 1

        # Update the core stat
        self._points += points
        self.restore()

        # Update the derived stat
        self.derived._base = self.base
        self.derived.restore()
        return True

    def restart(self):
        """ Removes all upgrades on this stat """
        old_points = self._points

        # Update the core stat
        self._points = 0
        self.restore()

        # Update the derived stat
        self.derived._base = self.base
        self.derived.restore()

        # Return what was removed for keeping track of stat restarts
        return old_points

    def restore(self):
        """ Restores the current value back to baseline """
        self.current = self._points + 1

    def __getstate__(self):
        """ Serialize core stat """
        return {
            "points": self._points,
            "derived_factor": self._derived.factor,
            "derived_offset": self._derived.offset
        }

    def __setstate__(self, state):
        """ Deserialize core stat """
        # Update the core stat
        self._points = state["points"]
        self.restore()

        # Update the derived stat
        factor = state["derived_factor"]
        offset = state["derived_offset"]
        self.set_derived(factor, offset)
        self.derived.restore()

class DerivedStat():
    """ Derived stats are based off core stats, and change when their core changes """
    def __init__(self, base, factor=1.0, offset=0):
        self._factor = factor
        self._offset = offset
        self._base = base
        self._current = self.base

    @property
    def base(self):
        """ Programmatically calculates the base value """
        return (self._base * self._factor) + self._offset

    @property
    def current(self):
        """ Update than grab the current value """
        return self._current

    @current.setter
    def current(self, value):
        """ Sets the current value """
        self._current = int(value)
        if self._current < 0:
            self._current = 0

    @property
    def factor(self):
        """ Get the multiplication factor """
        return self._factor

    @factor.setter
    def factor(self, value):
        """ Set the multiplication factor """
        value = int(value)
        if value < 1:
            value = 1

        self._factor = value
        return value

    @property
    def offset(self):
        """ Get the offset """
        return self._offset

    @offset.setter
    def offset(self, value):
        """ Set the addition offset """
        value = int(value)
        if value < 0:
            value = 0

        self._offset = value
        return value

    def restore(self):
        """ Restores the current value back to the given amount """
        self._current = self.base
