""" Import sub modules for direct API access """
import bot.api.battle
import bot.api.character
import bot.api.shop
import bot.api.errors

class API():
    def __init__(self, logger):
        self.logger = logger
        self.battle = bot.api.battle.BattleAPI(self)
        self.character = bot.api.character.CharacterAPI(self)
        self.shop = bot.api.shop.ShopAPI(self)
