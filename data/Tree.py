import logging
import random

from typing import List
from data.Contour import Contour
from data.Node import Node
from data.TreeAction import *
from logutils.DeferredMessage import DeferredMessage

log = logging.getLogger("pyfloorplanner")

class Tree:
    def __init__(self, root: Node, nodes: List[Node]):
        # TODO: build tree from nodes
        self.nodes = nodes
        self.root = root

        self.hor_cont = Contour()
        self.ver_cont = Contour()

        self.lastAction = TreeAction(self)

    def clone(self):
        pass

    def rotate(self):
        # TODO: fix that some nodes cannot be rotated
        node = random.choice(self.nodes)
        self.apply(Rotate(self, node))

    def move(self):
        pass

    def swap(self):
        pass

    def remove_soft(self):
        pass

    def remove(self, node):
        self.apply(Remove(self, node))

    def insert(self, node, parent):
        pass

    def revertLast(self):
        log.debug(f"Before revert: {self.lastAction.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

        self.lastAction.revert()

        log.debug(f"After revert: {self.lastAction.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

    # Calculate the area of the floorplan that belongs to the current tree
    def calc_area(self) -> float:
        pass

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
