import os
import sys
from bot import server

def main():
    """ Start the bot and have it wait for commands """
    service = server.BotService()
    service.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    sys.exit(main())
