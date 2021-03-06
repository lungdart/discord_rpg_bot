from discord import Embed


class NullLogger():
    """ Null logger to ignore all output """
    class NullEntry():
        def color(self, value):
            pass
        def title(self, value):
            pass
        def desc(self, value):
            pass
        def field(self, title, desc, inline=False):
            pass
        def buffer(self):
            pass
        def buffer_pm(self, name):
            pass

    def entry(self):
        return self.NullEntry()

class DiscordLogger():
    """ Embed based discord logger """
    class EmbedEntry():
        """ Wrapper for discords embed that also marks when it's ready to send """
        colors = {
            "default": 0x1d8ba3,
            "info"   : 0x1d8ba3,
            "warn"   : 0xffb132,
            "error"  : 0xc44445,
            "success": 0x43b581
        }

        def __init__(self, parent):
            self.embed = Embed(color=self.colors['default'])
            self.ready = False
            self.username = None

        def color(self, name):
            """ Set the embed color """
            if name not in self.colors:
                name = 'default'
            self.embed.color = self.colors[name]

        def title(self, value):
            """ Set's the embed's title """
            self.embed.title = value

        def desc(self, value):
            """ Set's the embed's description """
            self.embed.description = value

        def field(self, title, desc, inline=False):
            """ Adds a new field to the embed """
            self.embed.add_field(name=title, value=desc, inline=inline)

        def buffer(self):
            """ Marks the embed as ready to send to the channel """
            self.ready = True

        def buffer_pm(self, username):
            """ Marks the embed as ready to send as a PM to the given username """
            self.username = username
            self.ready = True

    def __init__(self, channel):
        self.channel = channel
        self.buffer = []
        self.timer = None

    def entry(self):
        """ Request a new logging entry """
        entry = self.EmbedEntry(self.channel)
        self.buffer.append(entry)
        return entry

    async def send_buffer(self):
        """ Sends off any finished entries in the logging cache """
        # Loop backwards, because we're deleting entries as we go
        for entry in list(self.buffer):

            # PM a username directly, and remove the log entry
            if entry.ready and entry.username:
                target = [x for x in self.channel.members if x.name == entry.username][0]
                await target.send(embed=entry.embed)
                self.buffer.remove(entry)
                continue

            # Message the channel and remove the log entry
            elif entry.ready:
                await self.channel.send(embed=entry.embed)
                self.buffer.remove(entry)
                continue
