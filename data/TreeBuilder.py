import random
from typing import List

from data.Module import Module
from data.Tree import Node, Tree


class TreeBuilder:
    @staticmethod
    def random_tree(modules: List[Module], seed=None) -> Tree:
        '''
        Creates a random tree for the given list of modules
        :param seed: Seed for randomness
        :param modules: list of modules for to create nodes
        :return: A B-tree
        '''
        random.seed(seed)

        nodes = [Node(m) for m in modules]
        queue = nodes.copy()
        random.shuffle(nodes)
        root = queue.pop()

        # (node, True) for indicating that the left child of node is free, (node, False) for the right child of node
        free_places = [(root, True), (root, False)]
        while len(queue) > 0:
            placement_node = queue.pop()

            free_place = random.choice(free_places)
            free_places.remove(free_place)

            parent, left = free_place

            # Place node in free place
            if left:
                parent.left = placement_node
            else:
                parent.right = placement_node

            placement_node.parent = parent

            free_places.extend([(placement_node, True), (placement_node, False)])

        return Tree(root, nodes)
