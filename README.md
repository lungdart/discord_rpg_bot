# discord_rpg_bot
RPG battle bot for discord

## Commands
### Battle Commands
The following commands are used within the context of a battle, either to manage it or interact with it.
| Command                | Scope   | Description                                      |
|------------------------|---------|--------------------------------------------------|
| ```!battle```          | CHANNEL | Create a new battle                              |
| ```!battle start```    | CHANNEL | Start a battle that has 2 or more participants   |
| ```!battle stop```     | CHANNEL | Stop a battle at any point. All progress is lost |
| ```!join```            | CHANNEL | Join a created battle ready for new participants |
| ```!attack <target>``` | PM      | Attack a target                                  |
| ```!defend```          | PM      | Defend against physical attacks                  |

### Out of battle
| Command                 | Scope | Description                           |
|-------------------------|-------|---------------------------------------|
| ```!stats```            | ANY   | Check your full stats                 |
| ```!stats <target>```   | ANY   | Check another characters full stats   |
| ```!shop```             | ANY   | View what's for sale in the shop      |
| ```!buy <target>```     | ANY   | Buy an item from the shop with gold   |
| ```!unequip <target>``` | ANY   | Unequip whatever is in the given slot |
| ```!equip <target>```   | ANY   | Equip gear that's in your inventory   |
