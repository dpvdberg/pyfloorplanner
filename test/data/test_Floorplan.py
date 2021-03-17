import random
from unittest import TestCase

from data.Floorplan import Floorplan
from data.Module import *
from data.TreeBuilder import TreeBuilder


class TestFloorplan(TestCase):

    def test_plot(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(4)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)

        print('T after construction')
        t.print()

        t.calc_area()

        fp = Floorplan(t)
        fp.plot(draw_tree=True, draw_contour=True)
