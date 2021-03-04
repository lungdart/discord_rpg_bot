""" User level battle commands """
import random
import threading
from statemachine import StateMachine, State
from bot.components import users
from bot.api.errors import CommandError

BATTLE = None
JOIN_WAIT_SECONDS = 60
TURN_WAIT_SECONDS = 60

class Battle(StateMachine):
    """ State Machine Handler """
    stopped = State('stopped', initial=True)
    joinable = State('Joinable')
    started = State('Started')

    round_started = State('Round started')
    round_wait = State('Waiting on input for round')
    round_running = State('Performing round')
    round_ended = State('Round ended')

    new = stopped.to(joinable)
    join = joinable.to.itself()
    start = joinable.to(started)

    new_round = started.to(round_started)
    wait_for_actions = round_started.to(round_wait)
    submit_action = round_wait.to.itself()
    run_round = round_wait.to(round_running)
    end_round = round_running.to(round_ended)
    next_round = round_ended.to(round_started)

    stop = stopped.from_(joinable, started, round_started, round_wait, round_running, round_ended)

    def __init__(self, logger):
        super(Battle, self).__init__()
        self.logger = logger
        self.round = 0
        self.participants = {}
        self.actions = {}
        self.turn_order = []
        self.death_order = []
        self.action_log = None

    def on_stop(self):
        """ When the current battle stops """
        self.round = 0
        self.participants = {}
        self.actions = {}
        self.turn_order = []
        self.death_order = []
        self.action_log = None

        log = self.logger.entry()
        log.title("Battle stopped")
        log.desc("The battle was stopped, any progress has been discarded.")
        log.send()

    def on_new(self):
        """ When a new battle is started """
        log = self.logger.entry()
        log.title("Battle Started!")
        log.desc("A new battle has started! Don't forget to join the battle if you'd like to participate")
        log.field(title="Commands", desc="!join\n!battle start\n!battle stop")
        log.send()

    def on_join(self, name):
        try:
            user = users.load(name)
        except FileNotFoundError:
            log = self.logger.entry()
            log.color("error")
            log.title("Join Error")
            log.desc(f"The character by the name {name} couldn't be loaded")
            log.send()
            return

        self.participants['name'] = user
        log = self.logger.entry()
        log.title(f"{name} has entered the battle field!")
        log.desc("TODO: User descriptions")
        log.send()

    def on_enter_started(self):
        """ The battle has begun it's first round """
        # Need 2 or more participants for a battle
        count = len(self.participants)
        if count < 2:
            log = self.logger.entry()
            log.color("warn")
            log.title("Battle Warning")
            log.desc(f"The battle can't be started until there are 2 or more participants. We currently have {count}.")
            log.field(title="Commands", desc="!join\n!battle stop")
            log.send()
            return

        self.new_round()

    def on_enter_round_started(self):
        """ A round has started """
        # Calculate the turn order and wait for actions
        self.round += 1
        self.turn_order = [k for k, v in sorted(self.participants.items(), key=lambda x: x[1].speed.current)]
        self.wait_for_actions()

        log = self.logger.entry()
        log.title(f"Begin Round {self.round}")
        log.description("Everyone PM the bot with your actions you'd like to take for the round")
        log.send()

        for name, user in self.participants():
            # Notify the user
            log = self.logger.entry()
            log.title(f"Waiting for round {self.round} action")
            log.desc("Remember to type your action in here. Once all actions are submitted the round results will be tallied and printed log in the channel")
            log.field(title="!attack", desc="!attack <target>\nPhysically attack the target", inline=True)
            log.field(title="!defend", desc="!defend\nDefending reduces any damage by half", inline=True)
            # log.field(title="!cast", value="!cast <spell> <target>\nCast a spell you have learned on the target. For more information type !spells", inline=True)
            # log.field(title="!use", value="!use <item> <target>\nUse an item on a target. For more information type !items", inline=True)
            log.pm(name)

            # Remove any lingering effects
            user.defending = False

        # Queue up a big log for all turn actions
        self.action_log = self.logger.entry()
        self.action_log.title(f"Round {self.round} results")

    def on_submit_action(self, name, action, **kwargs):
        """ Somebody submitted an action """
        # Get the source user (Action submitter)
        try:
            source_user = users.load(name)
        except FileNotFoundError:
            log = self.logger.entry()
            log.color("error")
            log.title("File not found")
            log.desc(f"The character data for {name} was not found!")
            log.send()
            return

        # Ensure the source user can make an action
        if not name in self.participants:
            log = self.logger.entry()
            log.color("warn")
            log.title("You're not in this battle")
            log.desc(f"Dont forget to join next time with the !join command")
            log.pm(name)
            return

        if name in self.actions:
            log = self.logger.entry()
            log.color("warn")
            log.title("Wait for the next round")
            log.desc("You have already used your turn this round. Please wait for the next round before submitting a new action.")
            log.pm(name)
            return

        if name in self.death_order:
            log = self.logger.entry()
            log.color("warn")
            log.title("You're dead!")
            log.desc("Pretty hard to submit a turn action from the grave! Better luck in the next battle.")
            log.pm(name)
            return

        # Ensure the optional target user can be targeted
        if 'target' in kwargs and not kwargs['target'] in self.participants:
            log = self.logger.entry()
            log.color("warn")
            log.title(f"{kwargs['target']} isn't a participant!")
            log.desc("Try targeting someone who's actually taking part!")
            log.field(title="!battle list", desc="List all battle participants")
            log.pm(name)
            return

        if 'target' in kwargs and kwargs['target'] in self.death_order:
            log = self.logger.entry()
            log.color("warn")
            log.title(f"{kwargs['target']} is dead!")
            log.desc("Don't beat a dead horse. Try picking a survivor instead...")
            log.field(title="!battle list", desc="List all battle participants")
            log.pm(name)
            return

        # If the user is alive and a participant but can't be loaded we have a serious issue
        try:
            kwargs['target_user'] = users.load(kwargs['target'])
        except KeyError:
            pass
        except FileNotFoundError:
            log = self.logger.entry()
            log.color("error")
            log.title("File not found")
            log.desc(f"The character data for {kwargs['target']} could not be found!")
            log.send()
            return

        if action == "attack":
            self.actions[name] = {
                "action": self._attack,
                "args": [source_user, kwargs['target_user']]
            }
        elif action == "defend":
            self.actions[name] = {
                "action": self._defend,
                "args": [source_user]
            }
        # elif action == "cast":
        #     self._cast(name, kwargs['spell'], kwargs['target'])
        # elif action == "use":
        #     self._use(name, kwargs['item'], kwargs['target'])
        else:
            log = self.logger.entry()
            log.color("warn")
            log.title(f"Bad action name {action}")
            log.desc("I don't know how to do that. Try something that works")
            log.field(title="!attack", desc="!attack <target>\nPhysically attack the target", inline=True)
            log.field(title="!defend", desc="!defend\nDefending reduces any damage by half", inline=True)
            log.pm(name)

        # Run the round actions once they are all submitted
        if len(self.actions) == len(self.participants):
            self.run_round()

    def on_run_round(self):
        """ Triggers when all actions are submitted and the round is run """
        # Run the actions in turn order for the round
        for name in self.turn_order:
            # Dead users skip over their turns
            if name in self.death_order:
                continue

            action = self.actions[name]['action']
            args = self.actions[name]['args']
            action(args)

        # Finally, send the entire round as a single log entry
        self.action_log.send()
        self.action_log = None

    def _attack(self, source, target):
        """ Source attacks target """
        # Get the relative strength ratio of the two targets
        physical_ratio = source.body / float(target.body)
        if target.defending:
            physical_ratio /= 2.0

        # Get the variable weapon power
        if not source.weapon:
            power = 1.0
        else:
            factor = random.uniform(source.weapon.min_factor, source.weapon.max_factor)
            power = source.weapon.power * factor

        # Damage is relative to power and physical strength ratio
        # TODO: Misses, Saves, Crits
        damage = int(power * physical_ratio)
        target.hurt(damage)

        # TODO: Custom weapon messages?
        self.action_log.field(
            title=f"{source.name} attacks {target.name}",
            desc=f"{source.name} deals {damage} to {target.name} with {source.weapon.name}")

        if not target.is_alive():
            self.death_order.append(target.name)
            # TODO: Custom death messages?
            self.action_log.field(
                title=f"{target.name} dies!",
                desc="It was nice knowing you..."
            )

    def _defend(self, source):
        """ Source defends """
        source.defending = True
        self.action_log.field(
            title=f"{source.name} defends for the turn",
            desc=f"{source.name} takes half damage for the rest of the round"
        )
