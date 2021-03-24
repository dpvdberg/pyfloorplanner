import logging
import random
import unittest
from unittest import TestCase

from data.Floorplan import Floorplan
from data.Module import *
from data.Node import Node
from data.Tree import Tree, Swap
from data.TreeBuilder import TreeBuilder

logging.basicConfig()

log = logging.getLogger("pyfloorplanner")


class TestTree(TestCase):
    def test_remove_propagate(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 18)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)
        t.revert_last()

    def test_remove_revert(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=3)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 18)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)
        t.revert_last()

    def test_remove_one_child(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 3)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)

    def test_remove_one_child_revert(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 3)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)
        t.revert_last()

    def test_remove_no_child(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 1)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)

    def test_remove_no_child_revert(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 1)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)
        t.revert_last()

    def test_remove_root(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 19)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)

    def test_remove_root_revert(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 19)

        print(f"removing node {n.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.remove(n)
        t.revert_last()

    def test_insert(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        n = Node(Module(str(21), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)))
        p = next(x for x in t.nodes if x.id == 6)
        insertLeft = True

        print(f"inserting node {n.id} under node {p.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.nodes.append(n)

        t.insert(n, p, insertLeft)

    def test_insert2(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        n = Node(Module(str(21), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)))
        p = next(x for x in t.nodes if x.id == 11)
        insertLeft = False

        print(f"inserting node {n.id} under node {p.id}")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.nodes.append(n)

        t.insert(n, p, insertLeft)

    def test_insert3(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        n = Node(Module(str(21), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)))
        p = None
        insertLeft = False

        print(f"inserting node {n.id} as root")
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.nodes.append(n)

        t.insert(n, p, insertLeft)

    def test_move(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        t.move()

    def test_swap_normal(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 11)
        v = next(x for x in t.nodes if x.id == 15)

        t.apply(Swap(t, u, v))

    def test_swap_normal_back(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 11)
        v = next(x for x in t.nodes if x.id == 15)

        t.apply(Swap(t, u, v))
        t.revert_last()

    def test_swap_root(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 11)
        v = next(x for x in t.nodes if x.id == 19)

        t.apply(Swap(t, u, v))

    def test_swap_no_children(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 6)
        v = next(x for x in t.nodes if x.id == 16)

        t.apply(Swap(t, u, v))

    def test_swap_descendant(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 18)
        v = next(x for x in t.nodes if x.id == 16)

        t.apply(Swap(t, u, v))

    def test_swap_descendant_root(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)
        logging.getLogger("pyfloorplanner").setLevel(logging.DEBUG)

        u = next(x for x in t.nodes if x.id == 18)
        v = next(x for x in t.nodes if x.id == 19)

        t.apply(Swap(t, u, v))

    def test_print(self):
        m1 = Module('a', ModuleType.HARD, Dimensions(1, 1), Vector2(0, 0))
        m2 = Module('b', ModuleType.HARD, Dimensions(1, 1), Vector2(0, 0))

        n2 = Node(m2)
        n1 = Node(m1, right=n2)

        t = Tree(n1, [n1, n2])
        t.print()

    def test_clone(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(2)
        n = next(x for x in t.nodes if x.id == 18)

        print(f"removing node {n.id}")

        t_clone = t.clone()

        print('T before modification')
        t.print()

        t.remove(n)

        print('T after modification')
        t.print()

        print('T clone')
        t_clone.print()

    def test_calc_area(self):
        modules = [Module(str(i), ModuleType.HARD, Dimensions(100, 100), Vector2(0, 0)) for i in range(20)]
        t = TreeBuilder.random_tree(modules, seed=1)

        random.seed(1)

        print('T after construction')
        t.print()

        t.calc_area()

        fp = Floorplan(t)
        fp.plot()
