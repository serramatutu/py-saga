from collections import Sequence
import asyncio

from pysaga.state import StatefulEntity, State
from pysaga.step import Step

class Saga(StatefulEntity):
    """A saga is a way to execute complex transactions across distributed systems while
        maintaining eventual consistency.
        
        Sagas are *asynchronous* by default."""

    def __init__(self, steps=None):
        if steps is None:
            steps = []
        if not isinstance(steps, Sequence):
            raise ValueError("Saga steps parameter must be array")
        
        self._steps = []
        for step in steps:
            self.add_step(step)

        super().__init__()
    
    def add_step(self, *args, **kwargs):
        # TODO: add support for method steps, HTTP steps etc
        step = Step.from_args(*args, **kwargs)
        if step is None:
            raise ValueError("Could not parse arguments into valid step type")
        self._steps.append(step)

    async def run(self, *args, executor=None, **kwargs):       
        loop = asyncio.get_event_loop()
        
        futures = [
            step.do_run(*args, **kwargs)
            for step in self._steps
        ]
        await asyncio.gather(*futures)

        failure = any([step.failure for step in self._steps])
        if failure:
            futures = [
                step.do_compensate(*args, **kwargs)
                for step in self._steps if step.success
            ]
            await asyncio.gather(*futures)
        
        self._state = State.FAILURE if failure else State.SUCCESS