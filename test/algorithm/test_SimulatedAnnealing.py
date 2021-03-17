from random import random
from unittest import TestCase

from algorithm.SimulatedAnnealing import SimulatedAnnealing
from data.Floorplan import Floorplan
from data.Module import Module, ModuleType, Dimensions, Vector2
from data.TreeBuilder import TreeBuilder


class TestSimulatedAnnealing(TestCase):
    def test_sa(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]

        sa = SimulatedAnnealing(modules, seed=1)
        sa.tree.print()

        totalArea = 100*100*20

        best = sa.sa(totalArea, 10, 10, 0.995, 0.0001)

        best.print()
        fp = Floorplan(best)
        fp.plot(draw_tree=True)

    def test_sa2(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(i*8, i*6), Vector2(0, 0)) for i in range(1, 20)]
        modules.append(Module("extra", ModuleType.HARD, Dimensions(200,10), Vector2(0,0)))

        sa = SimulatedAnnealing(modules, seed=1)
        sa.tree.print()

        totalArea = sum([i*8*i*6 for i in range(20)])

        best = sa.sa(totalArea, 50, 10, 0.995, 0.0001)

        best.print()
        fp = Floorplan(best)
        fp.plot(draw_tree=True, draw_contour=True)

    def test_sa_rotate(self):
        modules = [Module(str(0), ModuleType.HARD, Dimensions(200, 2), Vector2(0, 0)),
                   Module(str(1), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)),
                   Module(str(2), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)),
                   ]

        sa = SimulatedAnnealing(modules, seed=1)
        sa.tree.print()

        totalArea = 200*2 + 100*100 + 100*100

        best = sa.sa(totalArea, 10, 100, 0.99, 0.01)

        best.print()
        fp = Floorplan(best)
        fp.plot(draw_tree=True)




