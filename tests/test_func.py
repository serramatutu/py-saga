import asyncio
import unittest
from enum import Enum

from pysaga import Saga
from pysaga.func import FuncStep

class RunStatus:
    NOT_RUN = 0
    RUN = 1
    COMPENSATE = 2

class FuncTestCase(unittest.TestCase):
    def setUp(self):
        self.sync_val = RunStatus.NOT_RUN
        self.async_val = RunStatus.NOT_RUN

    def do_sync_step(self, success=True):
        def func():
            self.sync_val = RunStatus.RUN
            return success
        return func

    def compensate_sync_step(self):
        def func():
            self.sync_val = RunStatus.COMPENSATE
        return func

    def do_async_step(self, success=True):
        async def func():
            self.async_val = RunStatus.RUN
            return success
        return func

    def compensate_async_step(self):
        async def func():
            self.async_val = RunStatus.COMPENSATE
        return func

    def test_from_method_args(self):
        val = FuncStep.from_args(self.do_sync_step(), self.compensate_sync_step())
        self.assertIsInstance(val, FuncStep)

    def test_from_coroutine_args(self):
        val = FuncStep.from_args(self.do_async_step(), self.compensate_async_step())
        self.assertIsInstance(val, FuncStep)

    def test_from_invalid_args(self):
        val = FuncStep.from_args("not valid", "also not valid")
        self.assertIsNone(val)

    def test_init_from_invalid_args(self):
        self.assertRaises(ValueError, FuncStep, self.do_sync_step(), "not valid")
        self.assertRaises(ValueError, FuncStep, "not valid", self.compensate_sync_step())

    def test_run_ok(self):
        saga = Saga()
        saga.add_step(self.do_sync_step(True), self.compensate_sync_step())
        saga.add_step(self.do_async_step(True), self.compensate_async_step())

        asyncio.run(saga.run())

        self.assertTrue(saga.success)
        self.assertEquals(self.sync_val, RunStatus.RUN)
        self.assertEquals(self.async_val, RunStatus.RUN)

    def test_run_compensate(self):
        saga = Saga()
        saga.add_step(self.do_sync_step(True), self.compensate_sync_step())
        saga.add_step(self.do_async_step(False), self.compensate_async_step())

        asyncio.run(saga.run())

        self.assertTrue(saga.failure)
        self.assertEquals(self.sync_val, RunStatus.COMPENSATE)
        self.assertEquals(self.async_val, RunStatus.RUN)