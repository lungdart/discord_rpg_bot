""" Shopping commands """
from discord.ext import commands
from bot.components.logging import log_all

class Shop(commands.Cog):
    """ Shop commands """
    def __init__(self, api):
        self.api = api

    @commands.command()
    @log_all
    async def shop(self, ctx):
        """ View all items available in the shop """
        stuff = self.api.shop.list_all()
        weapons     = '\n'.join(stuff['weapons']) if stuff['weapons'] else 'None'
        armor       = '\n'.join(stuff['armor']) if stuff['armor'] else 'None'
        accessories = '\n'.join(stuff['accessories']) if stuff['accessories'] else 'None'
        items       = '\n'.join(stuff['items']) if stuff['items'] else 'None'
        spells      = '\n'.join(stuff['spells']) if stuff['spells'] else 'None'

        out = self.api.logger.entry()
        out.title('Welcome to the shop!')
        out.desc('Type *!info <ITEM>* to get more information about each item')
        out.field('Weapons', f'{weapons}')
        out.field('Armor', f'{armor}')
        out.field('Accessories', f'{accessories}')
        out.field('Items', f'{items}')
        out.field('Spells', f'{spells}')
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def info(self, ctx, *name):
        """ Get detailed information about an item """
        # Convert all additional parameters as a single name with spaces
        name = ' '.join(name)
        details = self.api.shop.find_info(name)

        # Parse the name and description as the embed title instead of a field
        out = self.api.logger.entry()
        out.title(f"{details['name']}")
        out.desc(f"{details['desc']}")

        # Parse the rest of the attributes as fields
        del details['name']
        del details['desc']
        for key in details:
            out.field(title=f'{key}', desc=f'{details[key]}')
        out.buffer(ctx.author)

        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def buy(self, ctx, *args):
        """ Purchase one or more item(s) from the shop """
        # Try to get the quantity as the final argument
        try:
            quantity = int(args[-1])
            args = args[:-1]
        except ValueError:
            quantity = 1

        # Get the full name of the item to buy as the rest of the arguments
        name = ' '.join(args)

        # Buy it/them
        user = self.api.character.get(ctx.author.name)
        self.api.shop.buy(user, name, quantity)
        cstats = self.api.character.stats(ctx.author.name)
        out = self.api.logger.entry()
        out.color('success')
        out.title(f"{quantity}x {name} purchased!")
        out.desc(f"You have {cstats['gold']} gold remaining...")
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')

    @commands.command()
    @log_all
    async def sell(self, ctx, *args):
        """ Sell one or more item(s) from your inventory """
        # Try to get the quantity as the final argument
        try:
            quantity = int(args[-1])
            args = args[:-1]
        except ValueError:
            quantity = 1

        # Get the full name of the item to buy as the rest of the arguments
        name = ' '.join(args)

        # Sell it/them
        user = self.api.character.get(ctx.author.name)
        self.api.shop.sell(user, name, quantity)
        cstats = self.api.character.stats(ctx.author.name)
        out = self.api.logger.entry()
        out.color('success')
        out.title(f"{quantity} {name} sold!")
        out.desc(f"You now have {cstats['gold']} gold!")
        out.buffer(ctx.author)
        await self.api.logger.send_buffer()
        await ctx.message.add_reaction(u'👍')
