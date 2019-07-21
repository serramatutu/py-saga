from inspect import iscoroutinefunction
from pysaga.step import AbstractStep, Step, AsyncStep

class FuncStep(Step):
    """Function call Saga step"""

    def __init__(self, func):
        if not isinstance(func, callable):
            raise ValueError("'func' argument must be callable")
        if iscoroutinefunction(func):
            raise ValueError(
                "Cannot instance FuncStep with asynchronous function. "
                "Use AsyncFuncStep for asynchronous step functions"
            )
        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @staticmethod
    def from_args(self, *args, **kwargs):
        if (len(args) == 0 or not isinstance(args[0], callable) 
            or iscoroutinefunction(args[0])):
            return None
        return FuncStep(args[0])

AbstractStep.register_step_class(FuncStep)

class AsyncFuncStep(AsyncStep):
    """Async function call Saga step"""

    def __init__(self, func):
        if not iscoroutinefunction(func):
            raise ValueError("'func' argument must be coroutine")
        self.func = func

    async def run(self, *args, **kwargs):
        return await self.func(*args, **kwargs)

    @staticmethod
    def from_args(self, *args, **kwargs):
        if len(args) == 0 or not iscoroutinefunction(args[0]):
            return None
        return AsyncFuncStep(args[0])

AbstractStep.register_step_class(AsyncFuncStep)