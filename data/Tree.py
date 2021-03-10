import random

from data.Contour import Contour
from data.Module import Module
from data.TreeAction import *


class Node:
    def __init__(self, value: Module, left: 'Node', right: 'Node', parent: 'Node'):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.rotated = False

class Tree:
    def __init__(self, root: Module, nodes: list[Module]):
        #TODO: build tree from nodes
        self.nodes = nodes
        self.root = root

        self.hor_cont = Contour()
        self.ver_cont = Contour()

        self.lastAction = TreeAction(self)

    def clone(self):
        pass

    def rotate(self):
        #TODO: fix that some nodes cannot be rotated
        node = random.choice(self.nodes)
        self.lastAction = Rotate(self, node)
        self.lastAction.do()

    def move(self):
        pass

    def swap(self):
        pass

    def remove_soft(self):
        pass

    def delete(self, node):
        pass

    def insert(self, node, parent):
        pass

    def revertLast(self):
        self.lastAction.revert()

    # Calculate the area of the floorplan that belongs to the current tree
    def calc_area(self) -> float:
        pass

    def feasible(self):
        return True
