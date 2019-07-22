from collections import Sequence
from pysaga.state import StatefulEntity, State
from pysaga.step import Step

class Saga(StatefulEntity):
    """A saga is a way to execute complex transactions across distributed systems while
        maintaining eventual consistency.
        
        Sagas are *asynchronous* by default. If you're executing a saga outside of
        an event loop, please use the SyncSaga class."""

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

    async def run(self):
        pass