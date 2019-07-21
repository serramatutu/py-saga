from abc import abstractmethod, abstractclassmethod
from enum import Enum

class StepState(Enum):
    SUCCESS     = 0
    COMPENSATED = 1
    FAILURE     = 2
    CREATED     = 3
    RUNNING     = 4

class AbstractStep:
    """Abstract saga step"""
    _step_classes = set()

    def __init__(self):
        self._state = StepState.CREATED

    @staticmethod
    def register_step_class(klass):
        AbstractStep._step_classes.add(klass)

    @staticmethod
    def from_args(self, *args, **kwargs):
        """Tries to instance a Step from args and kwargs.
            Returns: Step if args/kwargs are valid. Returns None otherwise"""
        if len(args) > 0 and isinstance(args[0], AbstractStep):
            return args[0]
        for klass in AbstractStep._step_classes:
            result = klass.from_args(*args, **kwargs)
            if result is not None:
                return result
        return None

    @property
    def state(self):
        return self._state

    @property
    def complete(self):
        return self._state in [StepState.COMPENSATED, StepState.SUCCESS, StepState.FAILURE]

    @property
    def success(self):
        return self._state in [StepState.COMPENSATED, StepState.SUCCESS]

    @property
    def failure(self):
        return self._state == StepState.FAILURE

class Step(AbstractStep):
    """Saga step that runs synchronously"""

    def do_run(self, *args, **kwargs):
        self._state = StepState.RUNNING
        success = self.run(*args, **kwargs)
        self._state = StepState.SUCCESS if success else StepState.FAILURE

    def do_compensate(self, *args, **kwargs):
        self.compensate(*args, **kwargs)
        self._state = StepState.COMPENSATED
    
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def compensate(self, *args, **kwargs):
        pass

class AsyncStep(AbstractStep):
    """Saga step that runs asynchronously"""

    async def do_run(self, *args, **kwargs):
        self._state = StepState.RUNNING
        success = await self.run(*args, **kwargs)
        self._state = StepState.SUCCESS if success else StepState.FAILURE

    async def do_compensate(self, *args, **kwargs):
        await self.compensate(*args, **kwargs)
        self._state = StepState.COMPENSATED
    
    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    @abstractmethod
    async def compensate(self, *args, **kwargs):
        pass