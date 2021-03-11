import logging
import random
from unittest import TestCase

from data.Module import *
from data.Node import Node
from data.Tree import Tree
from data.TreeBuilder import TreeBuilder

logging.basicConfig()

class TestTree(TestCase):
    def test_remove(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.from_modules(modules, seed=1)

        random.seed(1)
        n = next(x for x in t.nodes if x.id == 18)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)

    def test_print(self):
        m1 = Module('a', ModuleType.HARD, Dimensions(1, 1), Vector2(0, 0))
        m2 = Module('b', ModuleType.HARD, Dimensions(1, 1), Vector2(0, 0))

        n2 = Node(m2)
        n1 = Node(m1, right=n2)

        t = Tree(n1, [n1, n2])
        t.print()