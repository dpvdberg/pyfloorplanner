import logging
from typing import List
from data.Contour import Contour
from data.Node import Node
from data.TreeAction import *
from logutils.DeferredMessage import DeferredMessage

import random

log = logging.getLogger("pyfloorplanner")


class Tree:
    def __init__(self, root: Node, nodes: List[Node]):
        # TODO: build tree from nodes
        self.nodes = nodes
        self.root = root

        self.hor_cont = Contour()
        self.ver_cont = Contour()

        self.lastAction = TreeAction(self)

    def clone(self) -> 'Tree':
        root_clone = self.root.clone()
        return Tree(root_clone, root_clone.nodes_in_subtree())

    def rotate(self):
        # TODO: fix that some nodes cannot be rotated
        node = random.choice(self.nodes)
        self.apply(Rotate(self, node))

    def move(self):
        node = random.choice(self.nodes)
        parent = random.choice(self.nodes + [None])
        while parent == node:
            parent = random.choice(self.nodes + [None])
        insertLeft = random.choice([True, False])
        self.apply(Move(self, node, parent, insertLeft))

    def swap(self):
        first = random.choice(self.nodes)
        second = random.choice(self.nodes)
        self.apply(Swap(self, first, second))

    def remove_soft(self):
        pass

    def remove(self, node):
        self.apply(Remove(self, node))

    def insert(self, node, parent, insertLeft):
        self.apply(Insert(self, node, parent, insertLeft))

    def revertLast(self):
        log.debug(f"Before revert: {self.lastAction.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

        self.lastAction.revert()

        log.debug(f"After revert: {self.lastAction.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

    # Calculate the area of the floorplan that belongs to the current tree
    def calc_area(self) -> float:
        # Keep track of a stack that traverses the tree in DFS order
        stack = queue.LifoQueue()
        stack.put(self.root)
        while not stack:
            node = stack.get()
            if not node is None:
                self.calc_position(node)
                stack.put(node.right)
                stack.put(node.left)

        return self.hor_cont.get_max() * self.ver_cont.get_max()

    def feasible(self):
        return True

    def apply(self, action: TreeAction):
        self.lastAction = action

        log.debug(f"Before action: {action.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

        action.do()

        log.debug(f"After action: {action.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

    def to_text(self):
        # use binarytree package to allow easy printing
        from binarytree import Node as BNode

        bnodes = {n: BNode(n.id) for n in self.nodes}
        bnodes[None] = None

        # copy hierarchy
        for node, bnode in bnodes.items():
            if node is None:
                continue
            bnode.left = bnodes[node.left]
            bnode.right = bnodes[node.right]

        return str(bnodes[self.root])

    def print(self):
        print(self.to_text())

    def calc_position(self, n):
        pass
