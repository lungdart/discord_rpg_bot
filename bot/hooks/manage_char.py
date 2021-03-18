""" Character management commands """
from discord.ext import commands
from bot.components.logging import log_all

class ManageCharacter(commands.Cog):
    """ Character management commands """
    def __init__(self, api):
        self.api = api

    @commands.command()
    @log_all
    async def stats(self, ctx, target=None):
        """ Get your stats or the stats for someone else """
        if not target:
            target = ctx.author.name

        cstats = self.api.character.stats(target)

        level = f"""
        **Level**: {cstats['level']}
        **Experience**: {cstats['experience']}
        **Unspent Points**: {cstats['points']}"""
        derived = f"""
        **Life**: {cstats['current_life']}/{cstats['base_life']}
        **Mana**: {cstats['current_mana']}/{cstats['base_mana']}
        **Speed**: {cstats['current_speed']}/{cstats['base_speed']}"""
        core = f"""
        **Body**: {cstats['current_body']}/{cstats['base_body']}
        **Mind**: {cstats['current_mind']}/{cstats['base_mind']}
        **Agility**: {cstats['current_agility']}/{cstats['base_agility']}"""

        power_tough = f"{cstats['power']}/{cstats['toughness']}"

        out = self.api.logger.entry()
        out.title(f"Stats for {target}")
        out.desc(level)
        out.field("Derived Stats", derived)
        out.field("Core Stats", core)
        out.field("Power/Toughness", power_tough)
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def inventory(self, ctx, target=None):
        """ Get your inventory, or the inventory of someone else """
        # Grab the entire characters stats
        if not target:
            target = ctx.author.name
        cstats = self.api.character.stats(target)

        # Developped formatted output
        equipped = f"""
        **Weapon**: {cstats['weapon']}
        **Armor**: {cstats['armor']}
        **Accessory**: {cstats['accessory']}"""
        spells = ', '.join(cstats['spells']) if cstats['spells'] else 'None'
        stuff = "\n".join(cstats['inventory']) if cstats['inventory'] else 'None'
        gold = f"{cstats['gold']:,} Gold"

        # Output
        out = self.api.logger.entry()
        out.desc(equipped)
        out.field(title="Spells", desc=spells)
        out.field(title="Gold", desc=gold)
        out.field(title="Inventory", desc=stuff)
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def equip(self, ctx, *name):
        """ Equip an appropriate item into it's designated slot """
        # Converts multi word names into a single argument
        name = ' '.join(name)
        self.api.character.equip(ctx.author.name, name)

        out = self.api.logger.entry()
        out.color('success')
        out.title(f"You equipped {name}")
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def unequip(self, ctx, slot):
        """ Unequip an item from the given inventory slot """
        self.api.character.unequip(ctx.author.name, slot)

        out = self.api.logger.entry()
        out.color('success')
        out.title(f"Your {slot} is now empty")
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def upgrade(self, ctx, stat_name, points=1):
        """ Upgrade a core stat"""
        self.api.character.spend_points(ctx.author.name, stat_name, points)
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def restart(self, ctx):
        """ Upgrade a core stat"""
        self.api.character.restart_points(ctx.author.name)
        await ctx.message.add_reaction(u'👍')
