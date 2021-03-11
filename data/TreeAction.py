import queue
from random import random

from data.Node import Node


class TreeAction:
    def __init__(self, tree):
        self.tree = tree

    def do(self):
        pass

    def revert(self):
        pass


class Rotate(TreeAction):
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node = node

    def do(self):
        self.node.rotated = not self.node.rotated

    def revert(self):
        self.node.rotated = not self.node.rotated


class Remove(TreeAction):
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node = node
        self.propagation_order = queue.LifoQueue()

    def do(self):
        if self.node.has_two_children():
            # Move children up until we reach the bottom of the tree
            current_node = self.node

            # Determine whether to move left or right node up
            propagate_right = True if random() > 0.5 else False
            # Store propagation order in case of revert
            self.propagation_order.put(propagate_right)
            # Get node to move up
            replace_node = current_node.right if propagate_right else current_node.left
            # Get dangling node after move
            dangling_node = current_node.left if propagate_right else current_node.right
            # Do the replacement; set parent child pointer from current node to replace node
            current_node.parent.replace_child(current_node, replace_node)

            current_node = replace_node

            # Propagate down in random order
            while dangling_node is not None:
                propagate_right = True if random() > 0.5 else False
                self.propagation_order.put(propagate_right)

                new_dangling_node = current_node.right if propagate_right else current_node.left

                if propagate_right:
                    current_node.right = dangling_node
                else:
                    current_node.left = dangling_node

                current_node = dangling_node
                dangling_node = new_dangling_node

        else:
            # Node has one child or no child, replace
            self.node.parent.replace_child(self.node.get_first_child())

    def revert(self):
        # TODO: use propagation_order to revert removal
        pass


class Move(TreeAction):
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node = node
        self.orig_parent = node.parent

    def do(self):
        # TODO: delete and insert in random new place
        pass

    def revert(self):
        self.tree.remove(self.node)
        self.tree.insert(self.node, self.orig_parent)
