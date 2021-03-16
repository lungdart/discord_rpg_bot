""" Hooks the API into discord commands """
import os
import discord
from discord.ext import commands
import bot.components.logging
import bot.hooks
import bot.api

class BotService():
    """ Discord bot service """
    def __init__(self):
        # Discord components
        self.client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        self.logger = bot.components.logging.DiscordLogger()

        # API instance to handle discord calls and logic
        self.api = bot.api.API(self)

        # Connect hooks for commands
        self.client.add_cog(bot.hooks.Admin(self.api))
        self.client.add_cog(bot.hooks.Battle(self.api))
        self.client.add_cog(bot.hooks.ManageCharacter(self.api))
        self.client.add_cog(bot.hooks.Activities(self.api))
        self.client.add_cog(bot.hooks.Shop(self.api))

        # Manually connect event listeners
        self.client.event(self.on_ready)

    def start(self, token):
        """ Start the bot service """
        if not token:
            raise TypeError("Token can not be None")

        self.client.run(token, bot=True)

    async def on_ready(self):
        """ Triggers when the bot is ready """
        print("Connected!")

        # Create new characters for all members who don't have one
        all_members = [x.name for x in self.client.get_all_members()]
        self.api.character.create_missing(all_members)
