import logging
import queue
import random
from typing import Optional

from data.Node import Node
from logutils.DeferredMessage import DeferredMessage

log = logging.getLogger("pyfloorplanner")


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


class Move(TreeAction):
    def __init__(self, tree, node, parent, insertLeft):
        super().__init__(tree)
        self.node = node
        self.parent = parent
        self.insertLeft = insertLeft
        self.remove: TreeAction
        self.insert: TreeAction

    def do(self):
        self.remove = Remove(self.tree, self.node)
        self.remove.do()
        self.insert = Insert(self.tree, self.node, self.parent, self.insertLeft)
        self.insert.do()

    def revert(self):
        self.insert.revert()
        self.remove.revert()

class Swap(TreeAction):
    def __init__(self, tree, first: Node, second: Node):
        super().__init__(tree)
        self.first = first
        self.second = second

    def do(self):
        firstParent = self.first.parent
        secondParent = self.second.parent
        self.first.parent = secondParent
        self.second.parent = firstParent

        firstLeft = self.first.left
        secondLeft = self.second.left
        self.first.left = secondLeft
        self.second.left = firstLeft

        firstRight = self.first.right
        secondRight = self.second.right
        self.first.right = secondRight
        self.second.right = firstRight

    def revert(self):
        self.do()


class Remove(TreeAction):
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node: Node = node
        self.orig_parent: Node = self.node.parent
        self.propagation_order = queue.Queue()

    def do(self):
        if self.node.has_two_children():
            # Move children up until we reach the bottom of the tree
            current_node = self.node

            # Determine whether to move left or right node up
            propagate_right = True if random() > 0.5 else False
            # Get node to move up
            replace_node = current_node.right if propagate_right else current_node.left
            # Get dangling node after move
            dangling_node = current_node.left if propagate_right else current_node.right
            # Do the replacement; set parent child pointer from current node to replace node
            self.propagation_order.put(current_node.parent.replace_child(current_node, replace_node))
            # Store propagation order of the first child
            self.propagation_order.put(propagate_right)

            current_node = replace_node

            # log.debug("After initial replacement:")
            # log.debug(DeferredMessage(self.tree.to_text))

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

                # log.debug("After propagate:")
                # log.debug(DeferredMessage(self.tree.to_text))

            # log.debug("Propagation order:")
            # log.debug(DeferredMessage(lambda: str(list(self.propagation_order.queue))))
        else:
            # Node has one child or no child, replace
            self.propagation_order.put(self.node.parent.replace_child(self.node, self.node.get_first_child()))
            # Save position of original child
            self.propagation_order.put(self.node.has_right_child())

        # Set node as detached
        self.node.left = None
        self.node.right = None
        self.node.parent = None

    def revert(self):
        right_child = self.propagation_order.get()

        # Set original node back in tree position
        self.node.parent = self.orig_parent

        if right_child:
            dangling_child = self.orig_parent.right
            self.orig_parent.right = self.node
        else:
            dangling_child = self.orig_parent.left
            self.orig_parent.left = self.node

        # Set the first child of the original node back
        propagate_right = self.propagation_order.get()

        if propagate_right:
            self.node.right = dangling_child
        else:
            self.node.left = dangling_child

        first = True
        current_node = self.node
        last_placed_child = dangling_child
        previous_right = propagate_right

        while not self.propagation_order.empty():
            next_right = self.propagation_order.get()

            if next_right:
                next_child = last_placed_child.right
                last_placed_child.right = None
            else:
                next_child = last_placed_child.left
                last_placed_child.left = None

            # If we previously propagated right, it means the left node was dangling and this was propagated down.
            next_child.parent = current_node

            placed_right = previous_right
            # If this is the first propagation, we need to flip the placement
            placed_right = placed_right if not first else not placed_right

            if placed_right:
                current_node.right = next_child
            else:
                current_node.left = next_child

            previous_right = next_right
            current_node = last_placed_child
            last_placed_child = next_child
            first = False







class Insert(TreeAction):
    def __init__(self, tree, node: Node, parent: Optional['Node'], insertLeft: bool):
        super().__init__(tree)
        self.node = node
        self.parent = parent
        self.insertLeft = insertLeft

    def do(self):
        if self.parent is None:
            if self.insertLeft:
                self.node.left = self.tree.root
                self.tree.root = self.node
            else:
                self.node.right = self.tree.root
                self.tree.root = self.node
        elif self.insertLeft:
            if (self.parent.has_left_child()):
                oldChild = self.parent.left
                self.parent.replace_child(oldChild, self.node)
                self.node.parent = self.parent
                self.node.left = oldChild
            else:
                self.parent.left = self.node
                self.node.parent = self.parent
        else:
            if self.parent.has_right_child():
                oldChild = self.parent.right
                self.parent.replace_child(oldChild, self.node)
                self.node.parent = self.parent
                self.node.right = oldChild
            else:
                self.parent.right = self.node
                self.node.parent = self.parent

    def revert(self):
        if self.parent is None:
            if self.insertLeft:
                self.tree.root = self.node.left
                self.node.left = None
            else:
                self.tree.root = self.node.right
                self.node.right = None
        if self.insertLeft:
            if self.node.has_left_child():
                oldChild = self.node.left
                self.parent.replace_child(self.node, oldChild)
                self.node.parent = None
                self.node.left = None
            else:
                self.parent.left = None
                self.node.parent = None
        else:
            if self.node.has_right_child():
                oldChild = self.node.right
                self.parent.replace_child(self.node, oldChild)
                self.node.parent = None
                self.node.right = None
            else:
                self.parent.right = None
                self.node.parent = None

