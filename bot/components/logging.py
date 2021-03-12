""" Logging tools """
import sys
import functools
from datetime import datetime
from discord import Embed
from bot.api.errors import CommandError


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
        def buffer(self, ctx):
            pass

    def entry(self):
        return self.NullEntry()
    async def send_buffer(self):
        pass

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

        def __init__(self):
            self.embed = Embed(color=self.colors['default'])
            self.ready = False

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

        def buffer(self, target):
            """ Marks the embed as ready to send to the channel """
            self.ready = True
            self.target = target

        def buffer_pm(self, username):
            """ Marks the embed as ready to send as a PM to the given username """
            self.username = username
            self.ready = True

    def __init__(self):
        self.buffer = []
        self.timer = None

    def entry(self):
        """ Request a new logging entry """
        instance = self.EmbedEntry()
        self.buffer.append(instance)
        return instance

    async def send_buffer(self):
        """ Sends off any finished entries in the logging cache """
        # Loop backwards, because we're deleting entries as we go
        for entry in list(self.buffer):
            if entry.ready:
                await entry.target.send(embed=entry.embed)
                self.buffer.remove(entry)
                continue

def log_all(func):
    """ Command wrapper to automatically log everything """
    def log_out(command, author, *args, **kwargs):
        """ Logs events to stdout """
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        str_args = str(args)
        str_kwargs = str(kwargs)
        template = f"[{dt}] - {author} - !{command} *args={str_args}, **kwargs={str_kwargs}\n"
        sys.stdout.write(template)
        sys.stdout.flush()

    @functools.wraps(func)
    async def wrapper(self, ctx, *args, **kwargs):
        try:
            log_out(func.__name__, ctx.author.name, *args, **kwargs)
            return await func(self, ctx, *args, **kwargs)
        except CommandError as error:
            out = self.api.logger.entry()
            out.color('error')
            out.title('Command Error')
            out.desc(str(error))
            out.buffer_pm(ctx.channel)
            await self.api.logger.send_buffer()
            return
        except Exception as error:
            out = self.api.logger.entry()
            out.color('error')
            out.title('Unhandled Exception')
            out.desc(str(error))
            out.buffer(ctx.channel)
            await self.api.logger.send_buffer()
            raise error
    return wrapper
