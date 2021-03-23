import random
from unittest import TestCase

from data.Floorplan import Floorplan
from data.Module import *
from data.TreeBuilder import TreeBuilder


def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args, seed=i)

        return callHelper

    return repeatHelper


class TestFloorplan(TestCase):
    def test_plot(self, seed=3):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(10)]
        t = TreeBuilder.random_tree(modules, seed=seed)

        random.seed(1)

        t.calc_area()

        fp = Floorplan(t)
        fp.plot(draw_tree=True, draw_contour=True, contour_width=5)
