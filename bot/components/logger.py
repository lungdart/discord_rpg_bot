from discord import Embed

class LoggerFactory():
    """ Generates embed based logging instances """
    colors = {
        "info":    0x1d8ba3,
        "warn":    0xffb132,
        "error":   0xc44445,
        "success": 0x43b581
    }

    class Logger():
        """ Actual logger instance """
        def __init__(self, channel, title, color):
            """ Initializes the logging instance with the hidden channel object """
            self.channel = channel
            self.embed = Embed(title=title, color=color)

        def add(self, name, value, inline=False):
            """ Add's a new field to the embed message """
            self.embed.add_field(name=name, value=value, inline=inline)

        async def send(self):
            """ Send the embed to the battle channel """
            await self.channel.send(embed=self.embed)

        async def pm(self, username):
            """ Send the embed to the user """
            members = self.channel.members
            target = [x for x in members if x.name == username][0]
            await target.send(embed=self.embed)

    def __init__(self, channel):
        """ Initialize the factory with the channel object for logging to """
        self.channel = channel

    def __call__(self, title, color="info"):
        """ Generate a logging instance """
        color_hex = LoggerFactory.colors[color]
        instance = self.Logger(self.channel, title, color_hex)

        return instance
