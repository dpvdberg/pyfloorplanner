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
        best.calc_area()

        best.print()
        fp = Floorplan(best)
        fp.plot(draw_tree=True)

    def test_sa(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(i*8, i*6), Vector2(0, 0)) for i in range(20)]
        modules.append(Module("extra", ModuleType.HARD, Dimensions(200,10), Vector2(0,0)))

        sa = SimulatedAnnealing(modules, seed=1)
        sa.tree.print()

        totalArea = sum([i*8*i*6 for i in range(20)])

        best = sa.sa(totalArea, 10, 10, 0.995, 0.0001)
        area = best.calc_area()

        print(f"Area = {area}")

        best.print()
        fp = Floorplan(best)
        fp.plot(draw_tree=True)




