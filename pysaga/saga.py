from collections import Sequence
from pysaga.step import AbstractStep
    
class Saga:
    """Abstract Saga"""

    def __init__(self, steps=None):
        if steps is None:
            steps = []
        if not isinstance(steps, Sequence):
            raise ValueError("Saga steps parameter must be array")
        
        self._steps = []
        for step in steps:
            self.add_step(step)
    
    def add_step(self, *args, **kwargs):
        # TODO: add support for method steps, HTTP steps etc
        step = AbstractStep.from_args(*args, **kwargs)
        if step is None:
            raise ValueError("Could not parse arguments into valid step type")
        self._steps.append(step)