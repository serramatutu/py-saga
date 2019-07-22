from abc import abstractmethod, abstractclassmethod
from pysaga.state import StatefulEntity, State    

class Step(AbstractStep):
    """Saga step that runs asynchronously"""
    _step_classes = set()

    @staticmethod
    def register_step_class(klass):
        Step._step_classes.add(klass)

    @staticmethod
    def from_args(self, *args, **kwargs):
        """Tries to instance a Step from args and kwargs.
            Returns: Step if args/kwargs are valid. Returns None otherwise"""
        if len(args) > 0 and isinstance(args[0], Step):
            return args[0]
        for klass in Step._step_classes:
            result = klass.from_args(*args, **kwargs)
            if result is not None:
                return result
        return None

    async def do_run(self, *args, **kwargs):
        self._state = State.RUNNING
        success = await self.run(*args, **kwargs)
        self._state = State.SUCCESS if success else State.FAILURE

    async def do_compensate(self, *args, **kwargs):
        await self.compensate(*args, **kwargs)
        self._state = State.COMPENSATED
    
    @abstractmethod
    async def run(self, *args, **kwargs):
        pass

    @abstractmethod
    async def compensate(self, *args, **kwargs):
        pass