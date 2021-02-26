""" User level battle commands """
import random
import threading
from bot.components import users
from bot.api.errors import CommandError

class Battle():
    join_time = 60
    turn_time = 60

    def __init__(self, discord_logger):
        self.logger = discord_logger
        self.state = "stopped"
        self.users = {}

        self.round = 0
        self.round_limit = None
        self.round_results = []
        self.turn_usage = {}
        self.turn_order = []
        self.death_order = []

        self.join_timer = None
        self.turn_timer = None

    def start(self, round_limit=None):
        """ Starts a battle """
        if self._is_started():
            raise CommandError("There is already a battle started")

        self.state = "joinable"
        self.round_limit = round_limit
        self.join_timer = threading.Timer(Battle.join_time, Battle._join_timeout, args=self)

        output = self.logger(title="Battle", color="info")
        output.add(
            "A battle has begun!",
            f"""Type !join to enter this battle. Once everybody is ready, type !begin.
            After {Battle.join_time} seconds, the battle will automatically start"""
        )
        output.send()

    def stop(self, timeout=False):
        """ Stop a battle """
        if self._is_stopped():
            raise CommandError("There is no battle to stop")

        self.state = "stopped"
        self.users = {}

        self.round = 0
        self.round_limit = None
        self.turn_order = []

        output = self.logger(title="Battle", color="warn")
        if timeout:
            output.add(
                "Battle stopped",
                "The current battle was stopped because not enough users joined in time"
            )
        else:
            output.add(
                "Battle stopped",
                "The current battle was stopped prematurely by command"
            )
        output.send()

    def join(self, username):
        """ Join a user to this battle """
        if not self._is_joinable():
            raise CommandError("There is no battle ready to join")

        try:
            target = users.load(username)
        except FileNotFoundError:
            raise CommandError(f"{username} has no user character to join a battle with")

        self.users[username] = target

        output = self.logger(title="Battle", color="success")
        output.add(
            f"{username} joins the battle"
            f"TODO: Username descriptions"
        )
        output.send()

        output = self.logger(title="Battle", color="info")
        output.add(
            "Battle info",
            "When the battle begins, you will be asked to input your turn actions privately. Please be patient."
        )
        output.pm(username)

    def begin(self):
        """ Begins a battle with 2 or more people joined """
        if not self._is_joinable():
            raise CommandError("There is no battle waiting for users to begin")
        if self.users < 2:
            raise CommandError("There aren't enough users to start the battle")

        # _next_round() will take care of all the output
        self.state = "active"
        self._next_round()

    def attack(self, source, target):
        """ Have one user attack another """
        self._validate_can_act(source)

        if not target in self.users.keys():
            raise CommandError(f"{source} is not in this battle")


        # Damage is relative to weapon power, power range, body stat ratios
        modifier = source.body.current / float(target.body.current)
        randomizer = random.randint(source.weapon.min, source.weapon.max)
        damage = int(source.weapon.power * modifier * randomizer)
        if target.is_defending():
            damage = int(damage / 0.5)

        damage = max(damage, 1)
        died = target.hurt(damage)
        self.round_results.append({
            "title": f"{source} attacks {target}"
        })

        if died:
            self.round_results.append({
                "title": f"{target} dies",
            })
            self.death_order.append(target.name)
            del self.users[target.name]

        self._use_turn(source)

    def defend(self, source):
        """ Have a user defend """
        self._validate_can_act(source)

        source.is_defending(True)
        self.round_results.append({
            "title": f"{source} defends!"
        })

        self._use_turn(source)

    def use(self, source, target, skill):
        """ Have one user use a skill on another """
        self._validate_can_act(source)

        if not target in self.users.keys():
            raise CommandError(f"{target} is not in this battle")
        if not self._is_turn_wait():
            raise CommandError("Please wait for the current round to finish before inputting your next action")

        # TODO: Everything

        self.round_results.append({
            "title": f"{source} uses the {skill} skill on {target}"
        })

        self._use_turn(source)

    def item(self, source, target, item):
        """ Have one user use an item on another """
        self._validate_can_act(source)

        if not target in self.users.keys():
            raise CommandError(f"{target} is not in this battle")
        if not self._is_turn_wait():
            raise CommandError("Please wait for the current round to finish before inputting your next action")

        # TODO: Everything

        self.round_results.append({
            "title": f"{source} uses {item} on {target}"
        })

        self._use_turn(source)

    def cast(self, source, target, spell):
        """ Have one user cast a spell on another """
        self._validate_can_act(source)

        if not target in self.users.keys():
            raise CommandError(f"{target} is not in this battle")
        if not self._is_turn_wait():
            raise CommandError("Please wait for the current round to finish before inputting your next action")

        # TODO: Everything

        self.round_results.append({
            "title": f"{source} casts {spell} on {target}"
        })

        self._use_turn(source)

    def _join_timeout(self):
        """ Auto begins the battle after timeout """
        self.join_timer = None
        if len(self.users) >= 2:
            self.begin()
        else:
            self.stop(timeout=True)

    def _turn_timeout(self):
        """ Auto defends everything who hasn't inputted a command """
        self.turn_timer = None
        for user in self.users.keys():
            if user not in self.turn_order:
                self.defend(user)

        self.state = "active"

    def _validate_can_act(self, username):
        """ Validates that a user can act  """
        if not username in self.users.keys():
            raise CommandError(f"{username} is not in this battle")
        if not self._is_turn_wait():
            raise CommandError("Please wait for the current round to finish before inputting your next action")

        total_turns = self.turn_order.count(username)
        turn_count = self.turn_usage[username]
        if turn_count >= total_turns:
            raise CommandError(f"{username} doesn't have any turns left to spend")

    def _use_turn(self, username):
        """ Handles using up turns """
        self.turn_usage[username] += 1
        turns_left = self.turn_usage[username] - self.turn_order.count(username)

        output = self.logger(title="Battle", color="success")
        output.add(
            "Battle Command Success",
            f"Command successful. You have {turns_left} remaining for the round."
        )
        output.pm(username)

    def _next_round(self):
        """ Initiates the next round """
        self.state = "turn_wait"
        self.round += 1
        self.round_results = []
        self.turn_order = []

        if self.turn_timer:
            self.turn_timer.cancel()
        self.turn_timer = threading.Timer(Battle.turn_time, Battle._turn_timeout, args=self)

        output = self

    def _is_started(self):
        """ Checks if there's a battle started """
        return self.state != "stopped"

    def _is_stopped(self):
        """ Checks that there's no battle currently underway """
        return self.state == "stopped"

    def _is_joinable(self):
        """ Checks if the battle is joinable """
        return self.state == "joinable"

    def _is_active(self):
        """ Checks if the battle is ongoing """
        return self.state in ["active", "turn_wait"]

    def _is_turn_wait(self):
        """ Checks if the battle is waiting for turn inputs """
        return self.state == "turn_wait"
