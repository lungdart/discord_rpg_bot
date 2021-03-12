""" Battle commands """
from discord.ext import commands
from bot.components.logging import log_all

class Battle(commands.Cog):
    """ Battle commands """
    def __init__(self, api):
        self.api = api

    @commands.command()
    @log_all
    async def list(self, ctx):
        """ List battle participants """
        if self.api.battle.is_stopped:
            out = self.api.logger.entry()
            out.color("warn")
            out.title(f"No active battle")
            out.desc("There's no battle to list the participants from")
            out.buffer(ctx.channel)
            await self.api.logger.send_buffer()
            return

        # Seperate the living and the dead
        dead_list = self.api.battle.death_order
        alive_list = list(set(self.api.battle.participants).symmetric_difference(set(dead_list)))

        # Output
        out = self.api.logger.entry()
        out.title(f"Battle participants ({len(self.api.battle.participants)})")
        out.field("Alive", ", ".join(alive_list) if alive_list else "None")
        out.field("Dead", ", ".join(dead_list) if dead_list else "None")
        out.buffer(ctx.channel)
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def join(self, ctx):
        """ Join an active battle that's waiting for participants """
        if self.api.battle.is_joinable:
            user = self.api.character.get(ctx.author.name)
            self.api.battle.join(user)
        else:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle ready to join")
            log.desc("Wait for a new battle to be ready for participants")
            log.buffer(ctx.channel)

        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def attack(self, ctx, target_name):
        """ Attack a target while in battle """
        if self.api.battle.is_round_wait:
            source = self.api.character.get(ctx.author.name)
            target = self.api.character.get(target_name)
            self.api.battle.submit_action(source, 'attack', target=target)
        else:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle round waiting for turn actions")
            log.desc("Wait for the next round, or the next battle")
            log.buffer(ctx.channel)

        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def defend(self, ctx):
        """ Defend for the round while in battle """
        if self.api.battle.is_round_wait:
            source = self.api.character.get(ctx.author.name)
            self.api.battle.submit_action(source, 'defend')
        else:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle round waiting for turn actions")
            log.desc("Wait for the next round, or the next battle")
            log.buffer(ctx.channel)

        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def cast(self, ctx, spell_name, target_name):
        """ (NOT YET IMPLEMENTED) Cast a spell on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.channel)
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def item(self, ctx, item_name, target_name):
        """ (NOT YET IMPLEMENTED) Use an item on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.channel)
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def use(self, ctx, skill_name, target_name):
        """ (NOT YET IMPLEMENTED) Use an skill on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.channel)
        await self.api.logger.send_buffer()
