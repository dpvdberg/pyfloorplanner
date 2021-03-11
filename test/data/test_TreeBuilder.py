import logging
from unittest import TestCase

from data.Module import *
from data.TreeBuilder import TreeBuilder


class TestTreeBuilder(TestCase):
    def test_from_modules(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.from_modules(modules, seed=1)
        t.print()
