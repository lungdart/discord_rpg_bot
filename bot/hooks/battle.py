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
            out.buffer(ctx.author)
            await self.api.logger.send_buffer()
            await ctx.message.add_reaction(u'❌')
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
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def join(self, ctx):
        """ Join an active battle that's waiting for participants """
        if not self.api.battle.is_joinable:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle ready to join")
            log.desc("Wait for a new battle to be ready for participants")
            log.buffer(ctx.author)
            await self.api.logger.send_buffer()
            await ctx.message.add_reaction(u'❌')
            return

        user = self.api.character.get(ctx.author.name)
        self.api.battle.join(user)
        await ctx.message.add_reaction(u'👍')
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def attack(self, ctx, target_name):
        """ Attack a target while in battle """
        if not self.api.battle.is_round_wait:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle round waiting for turn actions")
            log.desc("Wait for the next round, or the next battle")
            log.buffer(ctx.author)
            await self.api.logger.send_buffer()
            await ctx.message.add_reaction(u'❌')
            return

        source = self.api.character.get(ctx.author.name)
        target = self.api.character.get(target_name)

        self.api.battle.submit_action(source, 'attack', target=target)
        await ctx.message.add_reaction(u'👍')
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def defend(self, ctx):
        """ Defend for the round while in battle """
        if not self.api.battle.is_round_wait:
            log = self.api.logger.entry()
            log.color("warn")
            log.title("There is no battle round waiting for turn actions")
            log.desc("Wait for the next round, or the next battle")
            log.buffer(ctx.authro)
            await self.api.logger.send_buffer()
            await ctx.message.add_reaction(u'❌')
            return

        source = self.api.character.get(ctx.author.name)
        self.api.battle.submit_action(source, 'defend')
        await ctx.message.add_reaction(u'👍')
        await self.api.logger.send_buffer()

    @commands.command()
    @log_all
    async def cast(self, ctx, spell_name, target_name):
        """ (NOT YET IMPLEMENTED) Cast a spell on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')

    @commands.command()
    @log_all
    async def item(self, ctx, item_name, target_name):
        """ (NOT YET IMPLEMENTED) Use an item on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')

    @commands.command()
    @log_all
    async def use(self, ctx, skill_name, target_name):
        """ (NOT YET IMPLEMENTED) Use an skill on a target """
        log = self.api.logger.entry()
        log.color("warn")
        log.title("Command not yet implemented")
        log.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'❌')

    @commands.Cog.listener()
    @log_all
    async def on_join_timeout(self, ctx):
        """ Handles a battle timing out while waiting for participants """
        count = len(self.api.battle.participants)
        log = self.api.logger.entry()
        if not count >= 2:
            log.color("error")
            log.title("Battle timed out")
            log.desc("Not enough participants joined the battle in the required time")
            log.buffer(ctx.channel)
            self.api.battle.stop()
            await self.api.logger.send_buffer()
            return

        log.color("warn")
        log.title("Battle timed out")
        log.desc(f"The window to join the battle has ended, the battle will now begin with {count} participants")
        log.buffer(ctx.channel)
        self.api.battle.start()
        await self.api.logger.send_buffer()

    @commands.Cog.listener()
    @log_all
    async def round_timeout(self, ctx):
        """ Remind users to give battle commands, force actions after a set amount of reminders """
        # After 3 reminders, the 4th reminder will force all defend actions
        self.api.battle.action_reminder_loop += 1
        count = len(self.api.battle.participants)
        log = self.api.logger.entry()
        if self.api.battle.action_reminder_loop == 4:
            log.color("error")
            log.title("Round timed out")
            log.desc(f"{count} participants will be forced to defend for the turn")
            log.buffer(ctx.channel)
            self.api.battle._defend_all()
            await self.api.logger.send_buffer()
            return

        log.color("warn")
        log.title("Waiting for participants")
        desc = f"The following {count} participants still haven't submitted an action for the round.\n"
        desc += "If no actions are submitted they will be forced to defend.\n\n"
        for participant in self.battle.unsubmitted_participants:
            desc += f"**{participant}**"
        log.desc(desc)
        log.buffer(ctx.channel)
        await self.api.logger.send_buffer()

        # Restart the timer
        self.api.timer_manager.create_timer("round_timeout", self.action_reminder_timeout, args=(self.ctx,))
