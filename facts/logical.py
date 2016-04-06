import asyncio
import logging
from collections import OrderedDict
from facts.grafts import Namespace, Loader
from facts.targeting import Target

__all__ = ['Logical']


class Logical:

    async def items(self):
        """Expose all grafts.
        """

        accumulator = Accumulator()
        for graft in Loader().run():
            accumulator.spawn(graft())
        response = await accumulator.join()
        return response.items()

    async def as_dict(self):
        data = await self.items()
        return OrderedDict(data)

    async def read(self, target):
        data = await self.as_dict()
        return Target(target).read(data)

    async def match(self, target):
        data = await self.as_dict()
        return Target(target).match(data)


class Accumulator:

    def __init__(self, *, loop=None):
        self.data = {}
        self.pending_tasks = 0
        self.loop = loop or asyncio.get_event_loop()
        self.future = asyncio.Future()
        self.processing = asyncio.Event(loop=self.loop)

    @property
    def ready(self):
        return self.pending_tasks <= 0

    def spawn(self, coro):
        self.processing.clear()
        task = asyncio.ensure_future(coro)
        task.add_done_callback(self._done)
        self.pending_tasks += 1
        return task

    def _done(self, future):
        try:
            response = future.result()
            data = self.data
            if isinstance(response, Namespace):
                namespace, response = response
                logging.info('Namespace %s', namespace)
                for part in Target(namespace):
                    data.setdefault(part, {})
                    data = data[part]

            # TODO allow nested namespace

            if response is not None:
                data.update(response)
        finally:
            self.pending_tasks -= 1
            if self.ready:
                self.processing.set()

    async def join(self):
        if not self.ready:
            await self.processing.wait()
        return self.data
