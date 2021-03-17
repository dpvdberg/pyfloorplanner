from random import random
from unittest import TestCase

from algorithm.SimulatedAnnealing import SimulatedAnnealing
from data.Module import Module, ModuleType, Dimensions, Vector2
from data.TreeBuilder import TreeBuilder


class TestSimulatedAnnealing(TestCase):
    def test_sa(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]

        sa = SimulatedAnnealing(modules, seed=1)
        sa.tree.print()

        totalArea = 100*100*20

        sa.sa(totalArea, 10, 2, 0.05, 0.1)


