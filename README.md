# discord_rpg_bot
RPG battle bot for discord

## Installation
This bot is designed to run in a container using docker.

### Requirements
#### Discord
Before running the container, you need to get the following information from discord
* App Token
* Guild ID
* Channel ID

#### Bot data
The bot comes with some basic data for inventory. Extend the data as you wish before running the bot to customize your instance.

The default data is found in `./data`

### Docker commands
#### Build the docker image
Run the following command to build the docker image
```bash
cd $PATH_TO_REPO
sudo docker build .
```

Once it's finished building you should see a new image without a repo or tag
```bash
sudo docker image list
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
<none>                  <none>              82dc8afb8e95        8 minutes ago       910MB
```

#### Run an instance
Using the `IMAGE ID` from above with the discord credentials, run a new instance of the container with the following variables
```bash
sudo docker run -d \
  --name discord_rpg_bot \
  -e DISCORD_TOKEN=$TOKEN \
  -e DISCORD_GUILD=$GUILD_ID \
  -e DISCORD_CHANNEL=$CHANNEL_ID \
  -v $PATH_TO_DATA:/data \
  --restart unless-stopped \
  $IMAGE_ID
```

## Commands
### Battle Commands
The following commands are used within the context of a battle, either to manage it or interact with it.
| Command            | Description                                      |
|--------------------|--------------------------------------------------|
| `!battle`          | Create a new battle                              |
| `!battle list`     | List all battle participants                     |
| `!battle start`    | Start a battle that has 2 or more participants   |
| `!battle stop`     | Stop a battle at any point. All progress is lost |
| `!join`            | Join a created battle ready for new participants |
| `!attack <target>` | Attack a target                                  |
| `!defend`          | Defend against physical attacks                  |

## Character Management
| Command               | Description                           |
|-----------------------|---------------------------------------|
| `!stats`              | Check your stats                      |
| `!stats <target>`     | Check another characters stats        |
| `!inventory`          | Check your inventory                  |
| `!inventory <target>` | Check another characters inventory    |

## Shopping
| Command               | Description                           |
|-----------------------|---------------------------------------|
| `!shop`               | View what's for sale in the shop      |
| `!buy <target>`       | Buy an item from the shop with gold   |
| `!unequip <target>`   | Unequip whatever is in the given slot |
| `!equip <target>`     | Equip gear that's in your inventory   |
