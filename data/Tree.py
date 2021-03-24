import logging
from typing import List

from data.Common import Vector2, Interval
from typing import List, Tuple
from data.Contour import Contour
from data.Node import Node
from data.TreeAction import *
from logutils.DeferredMessage import DeferredMessage
import networkx as nx

import random

log = logging.getLogger("pyfloorplanner")


class Tree:
    def __init__(self, root: Node, nodes: List[Node]):
        # TODO: build tree from nodes
        self.nodes = nodes
        self.root = root

        self.hor_cont = Contour()

        self.last_action = TreeAction(self)

    def validate_parents(self) -> bool:
        return self.root.validate_parents()

    def clone(self) -> 'Tree':
        root_clone = self.root.clone()
        return Tree(root_clone, root_clone.nodes_in_subtree())

    def rotate(self):
        # TODO: fix that some nodes cannot be rotated
        node = random.choice(self.nodes)
        self.apply(Rotate(self, node))

    def move(self):
        node = random.choice(self.nodes)
        # node = self.nodes[1]
        parent = random.choice(self.nodes + [None])
        # parent = self.nodes[34]
        while parent is node:
            parent = random.choice(self.nodes + [None])

        insert_left = random.random() > 0.5
        self.apply(Move(self, node, parent, insert_left))

    def swap(self):
        first = random.choice(self.nodes)
        second = random.choice(self.nodes)
        while second is first:
            second = random.choice(self.nodes)
        self.apply(Swap(self, first, second))

    def remove_soft(self):
        pass

    def remove(self, node):
        self.apply(Remove(self, node))

    def insert(self, node, parent, insertLeft):
        self.apply(Insert(self, node, parent, insertLeft))

    def revert_last(self):
        log.debug(f"Before revert: {self.last_action.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

        self.last_action.revert()

        log.debug(f"After revert: {self.last_action.__class__.__name__}")
        log.debug(DeferredMessage(self.to_text))

    # Calculate the area of the floorplan that belongs to the current tree
    def calc_area(self) -> float:
        # Keep track of a stack that traverses the tree in DFS order
        self.hor_cont = Contour()
        for node in self.root.dfs():
            self.calc_position(node)

        return self.hor_cont.get_max_y() * self.hor_cont.get_max_x()

    def feasible(self):
        return True

    def apply(self, action: TreeAction):
        self.last_action = action

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

    def to_networkx(self) -> Tuple[nx.DiGraph, map]:
        G = nx.DiGraph()
        pos = {}
        for n in self.nodes:
            dim = n.value.dimensions.to_vector()
            if n.rotated:
                dim = Vector2(dim.y, dim.x)

            pos[n.id] = (n.value.position + 0.5 * dim).to_tuple()
            if n.has_left_child():
                G.add_edge(n.id, n.left.id)
            if n.has_right_child():
                G.add_edge(n.id, n.right.id)

        return G, pos

    def print(self):
        print(self.to_text())

    def calc_position(self, n: Node):
        if self.root is n:
            n.value.position = Vector2(0, 0)

            dimensions = n.value.dimensions
            if n.rotated:
                node_width = dimensions.height
                node_height = dimensions.width
            else:
                node_width = dimensions.width
                node_height = dimensions.height

            self.hor_cont.insert(0, node_width, node_height)
            return

        parent = n.parent
        if n is parent.left:
            parent_width = parent.value.dimensions.width if not parent.rotated else parent.value.dimensions.height
            x = parent.value.position.x + parent_width
        elif n is parent.right:
            x = parent.value.position.x
        else:
            raise Exception("Tree structure is broken. Parent node does not have node as its child.")

        dimensions = n.value.dimensions
        if n.rotated:
            node_width = dimensions.height
            node_height = dimensions.width
        else:
            node_width = dimensions.width
            node_height = dimensions.height

        y = self.hor_cont.insert(x, x + node_width, node_height)
        n.value.position = Vector2(x, y)