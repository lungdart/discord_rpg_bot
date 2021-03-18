""" Admin commands """
from discord.ext import commands
from bot.components.logging import log_all

class Admin(commands.Cog):
    """ Admininstrator Commands """
    def __init__(self, api):
        self.api = api

    @commands.command()
    @log_all
    async def battle(self, ctx, command=None):
        """ Manage a battle instance """
        # No arguments indicates starting a battle
        if not command:
            self.api.battle.new(ctx)
            await ctx.message.add_reaction(u'👍')
        elif command == "start":
            self.api.battle.start()
            await ctx.message.add_reaction(u'👍')
        elif command == "stop":
            self.api.battle.stop()
            await ctx.message.add_reaction(u'👍')

        # Bad command
        else:
            out = self.api.logger.entry()
            out.color("error")
            out.title(f"Bad battle command {command}")
            out.desc("Did you mean to use one of the following valid commands instead")
            out.field(
                title="Commands",
                desc="""
                    **!battle**: Begins a new battle
                    **!battle *list* **: Lists battle participants
                    **!battle *start* **: Starts a battle if there are enough participants
                    **!battle *stop* **: Stops a battle at any point. All progress is lost
                """)
            out.buffer(ctx.author)
            await ctx.message.add_reaction(u'❌')

        # Send everything from the buffer
        await self.api.logger.send_buffer()
