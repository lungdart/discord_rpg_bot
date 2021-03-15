""" Activity commands """
from discord.ext import commands
from bot.components.logging import log_all

class Activities(commands.Cog):
    """ Activity Commands """
    def __init__(self, api):
        self.api = api

    @commands.command()
    @log_all
    async def work(self, ctx):
        """ (NOT YET IMPLEMENTED) Work while idle to earn gold """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')

    @commands.command()
    @log_all
    async def explore(self, ctx):
        """ (NOT YET IMPLEMENTED) Explore while idle to find loot """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')

    @commands.command()
    @log_all
    async def train(self, ctx):
        """ (NOT YET IMPLEMENTED) Train while idle to gain experience """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')
