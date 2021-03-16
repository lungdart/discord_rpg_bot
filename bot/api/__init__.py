""" Import sub modules for direct API access """
import bot.api.battle
import bot.api.character
import bot.api.shop
import bot.api.errors
import bot.components.timer

class API():
    """ Logic handler """
    def __init__(self, client=None, logger=None):
        # Capture the discord level components for API use
        # Default to a null logger for testing
        if not logger:
            self.logger = bot.components.logging.NullLogger()
        else:
            self.logger = logger

        # Default to a null timer for testing
        if not client:
            self.timer_factory = bot.components.timer.TimerFactory(
                bot.components.timer.NullTimer)
        else:
            self.timer_factory = bot.components.timer.TimerFactory(
                bot.components.timer.AsyncEventTimer,
                client)

        # Bot api stuff
        self.battle = bot.api.battle.BattleAPI(self)
        self.character = bot.api.character.CharacterAPI(self)
        self.shop = bot.api.shop.ShopAPI(self)
