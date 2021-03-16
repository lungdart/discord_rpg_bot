""" Import sub modules for direct API access """
import bot.api.battle
import bot.api.character
import bot.api.shop
import bot.api.errors

class API():
    """ Logic handler """
    def __init__(self, service):
        # Capture the discord level components for API use
        self.client = service.client
        self.logger = service.logger

        # Bot api stuff
        self.battle = bot.api.battle.BattleAPI(self)
        self.character = bot.api.character.CharacterAPI(self)
        self.shop = bot.api.shop.ShopAPI(self)
