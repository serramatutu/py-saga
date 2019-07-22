from inspect import isawaitable
from pysaga.step import Step
from concurrent.futures import ProcessPoolExecutor
import asyncio

class FuncStep(AsyncStep):
    """Function call Saga step. The function may be synchronous or asynchronous"""

    def __init__(self, func):
        if not isinstance(func, callable):
            raise ValueError("'func' argument must be callable")
        self.func = func

    async def run(self, *args, event_loop=None, executor=None, **kwargs):
        if isawaitable(self.func):
            return await self.func(*args, **kwargs)
        
        if executor is None:
            executor = ProcessPoolExecutor()
        if event_loop is None:
            event_loop = asyncio.get_event_loop()

        return await event_loop.run_in_executor(executor, self.func, *args, **kwargs)

    @staticmethod
    def from_args(self, *args, **kwargs):
        if len(args) == 0 or not isinstance(args[0], callable):
            return None
        return FuncStep(args[0])

Step.register_step_class(FuncStep)