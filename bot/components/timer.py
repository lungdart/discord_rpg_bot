import asyncio

class AsyncEventTimer():
    """ Timer that fires a discord event asynchronously on timeout """
    def __init__(self, client, name, timeout, args=None, kwargs=None):
        self.client  = client
        self.name    = name
        self.timeout = timeout
        self.args    = args or tuple()
        self.kwargs  = kwargs or {}

        self._task   = None
        print(f"Timer {self.name} initialized")

    def start(self):
        """ Start the timer """
        self._task = self.client.loop.create_task(self._run())

        # Return self to allow chaining start on construction
        return self

    def cancel(self):
        """ Cancel a timer that hasn't triggered yet """
        if not self.is_running():
            raise Exception("You can't cancel a timer that isn't running")

        self._task.cancel()

    def is_running(self):
        """ Is the timer running? """
        return self._task is not None and not self._task.done()

    async def _run(self):
        """ asynchronous call that is run when the timeout occurs """
        await asyncio.sleep(self.timeout)
        self.client.dispatch(self.name, *self.args, **self.kwargs)
