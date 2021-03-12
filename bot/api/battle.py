""" User level battle commands """
import random
from threading import Timer
from statemachine import StateMachine, State
from bot.api.errors import CommandError

class BattleAPI(StateMachine):
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

    def __init__(self, parent):
        super(BattleAPI, self).__init__()
        self._parent = parent
        self.ctx = None

        self.round = 0
        self.participants = {}
        self.actions = {}
        self.turn_order = []
        self.death_order = []
        self.action_log = None

        # Battle timers
        self.join_timeout = 60
        self.action_reminder_timeout = 10
        self.action_reminder_loops = 6
        self.timer = None

    def on_stop(self, timeout=False):
        """ When the current battle stops """
        # Cancel any timeouts
        if self.timer:
            self.timer.cancel()
        self.timer = None

        # Inform the public
        log = self._parent.logger.entry()
        log.title("Battle stopped")
        log.buffer(self.ctx.channel)

        # Reset state
        self.ctx = None
        self.round = 0
        self.participants = {}
        self.actions = {}
        self.turn_order = []
        self.death_order = []
        self.action_log = None

    def on_new(self, ctx):
        """ When a new battle is started """
        # Saving the context is important, because that's how we figure out where to send the logging messages
        self.ctx = ctx

        #TODO: Have a timer auto stop if nobody joins
        # Async HELL

        log = self._parent.logger.entry()
        log.title("Battle Started!")
        log.desc("A new battle has started! Don't forget to join the battle if you'd like to participate")
        log.field(title="Commands", desc="!join\n!battle start\n!battle stop")
        log.buffer(self.ctx.channel)

    def on_join(self, source):
        """ Triggered when a user joins the battle """
        # They shouldn't be able to join twice
        if source.name in self.participants:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title(f"You're already in the battle, {source.name}")
            log.desc("Just be patient, it will begin soon")
            log.buffer(self.ctx.channel)
            return

        self.participants[source.name] = source
        log = self._parent.logger.entry()
        log.title(f"{source.name} has entered the battle field!")
        log.desc("TODO: User descriptions")
        log.buffer(self.ctx.channel)

    def on_enter_started(self):
        """ The battle has begun it's first round """
        # Cancel the join wait timeout
        if self.timer:
            self.timer.cancel()
        self.timer = None

        # Need 2 or more participants for a battle
        count = len(self.participants)
        if count < 2:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title("Battle Warning")
            log.desc(f"The battle can't be started until there are 2 or more participants. We currently have {count}.")
            log.field(title="Commands", desc="!join\n!battle stop")
            log.buffer(self.ctx.channel)
            return

        self.new_round()

    def on_enter_round_started(self):
        """ A round has started """
        # Calculate the turn order and wait for actions
        self.round += 1
        self.turn_order = [k for k, v in sorted(self.participants.items(), key=lambda x: x[1].speed.current)]
        self.actions = {}

        # Wait for round actions
        self.wait_for_actions()

    def on_wait_for_actions(self):
        """ Inform the channel and each participant they are waiting for turn inputs """
        # Begin a round log
        self.action_log = self._parent.logger.entry()
        self.action_log.title(f"Round {self.round} results")

        # Continually bug the channel for actions
        self.announce_round_wait()

    def on_submit_action(self, source, action, **kwargs):
        """ Somebody submitted an action """
        # Ensure the source user can make an action
        if not source.name in self.participants:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title("You're not in this battle")
            log.desc(f"Dont forget to join next time with the !join command")
            log.buffer(self.ctx.channel)
            return

        if source.name in self.actions:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title("Wait for the next round")
            log.desc("You have already used your turn this round. Please wait for the next round before submitting a new action.")
            log.buffer(self.ctx.channel)
            return

        if source.name in self.death_order:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title("You're dead!")
            log.desc("Pretty hard to submit a turn action from the grave! Better luck in the next battle.")
            log.buffer(self.ctx.channel)
            return

        # Ensure the optional target user can be targeted
        if 'target' in kwargs and not kwargs['target'].name in self.participants:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title(f"{kwargs['target']} isn't a participant!")
            log.desc("Try targeting someone who's actually taking part!")
            log.field(title="!battle list", desc="List all battle participants")
            log.buffer(self.ctx.channel)
            return

        if 'target' in kwargs and kwargs['target'].name in self.death_order:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title(f"{kwargs['target']} is dead!")
            log.desc("Don't beat a dead horse. Try picking a survivor instead...")
            log.field(title="!battle list", desc="List all battle participants")
            log.buffer(self.ctx.channel)
            return

        if action == "attack":
            self.actions[source.name] = {
                "action": self._attack,
                "args": [source, kwargs['target']]
            }
        elif action == "defend":
            self.actions[source.name] = {
                "action": self._defend,
                "args": [source]
            }
        # elif action == "cast":
        #     self._cast(name, kwargs['spell'], kwargs['target'])
        # elif action == "use":
        #     self._use(name, kwargs['item'], kwargs['target'])
        else:
            log = self._parent.logger.entry()
            log.color("warn")
            log.title(f"Bad action name {action}")
            log.desc("I don't know how to do that. Try something that works")
            log.field(title="!attack", desc="!attack <target>\nPhysically attack the target", inline=True)
            log.field(title="!defend", desc="!defend\nDefending reduces any damage by half", inline=True)
            log.buffer(self.ctx.channel)

        # Run the round actions once they are all submitted
        if len(self.actions) == len(self.participants):
            self.run_round()

    def on_enter_round_running(self):
        """ Triggers when all actions are submitted and the round is run """
        # Run the actions in turn order for the round
        for name in self.turn_order:
            # Dead users skip over their turns
            if name in self.death_order:
                continue

            action = self.actions[name]['action']
            args = self.actions[name]['args']
            action(*args)

        # Finally, send the entire round as a single log entry
        self.action_log.buffer(self.ctx.channel)
        self.action_log = None
        self.end_round()

    def on_enter_round_ended(self):
        """ Triggers when a round has ended """
        # Remove any expired effects
        for name in self.participants:
            self.participants[name].defending = False

        # TODO: Winner winner chicken dinner
        if len(self.death_order) == len(self.participants) - 1:
            self.stop()

        # TODO: Tie game
        elif len(self.death_order) == len(self.participants):
            self.stop()

        # Continue as per normal
        else:
            self.next_round()

    def _attack(self, source, target):
        """ Source attacks target """
        # Get the relative strength ratio of the two targets
        physical_ratio = source.body.current / float(target.body.current)
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
        damage = max(1, int(power * physical_ratio))
        target.life.current -= damage

        # TODO: Custom weapon messages?
        self.action_log.field(
            title=f"{source.name} attacks {target.name}",
            desc=f"{source.name} deals {damage} to {target.name} with {source.weapon.name if source.weapon else 'EMPTY'}")

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

    def announce_round_wait(self):
        """ Announce to the channel that the bot is waiting for actions """
        submitted = [x for x in self.actions]
        waiting_on = [x for x in self.participants if not x in submitted]
        waiting_on_text = '\n'.join(waiting_on)

        log = self._parent.logger.entry()
        log.title(f"Waiting for actions from {len(waiting_on)} participants...")
        log.desc(f"{waiting_on_text}\n\nUse one of the following commands to submit an action:")
        log.field(title="!attack", desc="!attack <target>\nPhysically attack the target", inline=True)
        log.field(title="!defend", desc="!defend\nDefending reduces any damage by half", inline=True)
        # log.field(title="!cast", value="!cast <spell> <target>\nCast a spell you have learned on the target. For more information type !spells", inline=True)
        # log.field(title="!use", value="!use <item> <target>\nUse an item on a target. For more information type !items", inline=True)
        log.buffer(self.ctx.channel)
