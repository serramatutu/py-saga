from inspect import iscoroutinefunction
from pysaga.step import Step
import asyncio

class FuncStep(Step):
    """Function call Saga step. The function may be synchronous or asynchronous"""

    def __init__(self, func, compensation):
        if not callable(func):
            raise ValueError("'func' argument must be callable")
        if not callable(compensation):
            raise ValueError("'compensation' argument must be callable")

        self.func = func
        self.compensation = compensation
        super().__init__()

    async def _run_func(self, func, *args, executor=None, **kwargs):
        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, func, *args, **kwargs)
    
    async def run(self, *args, **kwargs):
        return await self._run_func(self.func, *args, **kwargs)

    async def compensate(self, *args, **kwargs):
        return await self._run_func(self.compensation, *args, **kwargs)

    @staticmethod
    def from_args(*args, **kwargs):
        if len(args) <= 1 or not callable(args[0]) or not callable(args[1]):
            return None
        return FuncStep(args[0], args[1])

Step.register_step_class(FuncStep)