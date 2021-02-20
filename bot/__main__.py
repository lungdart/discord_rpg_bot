import os
import sys
from . import hooks

def main():
    """ Start the bot and have it wait for commands """
    hooks.start_client(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    sys.exit(main())
