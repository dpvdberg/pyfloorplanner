import logging
import queue
from random import random
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
        self.do()


class Move(TreeAction):
    def __init__(self, tree, node, parent, insert_left):
        super().__init__(tree)
        self.node = node
        self.parent = parent
        self.insert_left = insert_left
        self.remove: TreeAction
        self.insert: TreeAction

    def do(self):
        log.debug(f"moving node {self.node.id}")

        self.remove = Remove(self.tree, self.node)
        self.remove.do()
        self.insert = Insert(self.tree, self.node, self.parent, self.insert_left)
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
        log.debug(f"swapping node {self.first.id} and {self.second.id}")

        first_is_root = self.first.parent is None
        second_is_root = self.second.parent is None

        first_has_second = self.first.has_child(self.second)
        second_has_first = self.second.has_child(self.first)

        first_parent = self.first.parent
        second_parent = self.second.parent
        if not first_is_root and not second_has_first:
            first_parent.replace_child(self.first, self.second)
        if not second_is_root and not first_has_second:
            second_parent.replace_child(self.second, self.first)

        self.first.parent = second_parent if not first_has_second else self.second
        self.second.parent = first_parent if not second_has_first else self.first

        first_left = self.first.left
        second_left = self.second.left
        if first_left is not None and self.first.left is not self.second:
            first_left.parent = self.second
        if second_left is not None and self.second.left is not self.first:
            second_left.parent = self.first

        self.first.left = second_left if second_left is not self.first else self.second
        self.second.left = first_left if first_left is not self.second else self.first

        first_right = self.first.right
        second_right = self.second.right
        if first_right is not None and self.first.right is not self.second:
            first_right.parent = self.second
        if second_right is not None and self.second.right is not self.first:
            second_right.parent = self.first

        self.first.right = second_right if second_right is not self.first else self.second
        self.second.right = first_right if first_right is not self.second else self.first

        if self.tree.root is self.first:
            self.tree.root = self.second
        elif self.tree.root is self.second:
            self.tree.root = self.first

    def revert(self):
        self.do()


class Remove(TreeAction):
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node: Node = node
        self.is_root = self.tree.root is self.node
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
            if self.is_root:
                # Place Nonce token if we are removing the root
                self.propagation_order.put(None)
                # Set new root in tree
                self.tree.root = replace_node
            else:
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
            new_child = self.node.get_first_child()
            # Node has one child or no child, replace
            self.propagation_order.put(self.node.parent.replace_child(self.node, new_child))
            # Update parent pointers
            if new_child:
                new_child.parent = self.node.parent
            # Save position of original child
            self.propagation_order.put(self.node.has_right_child())

        # Set node as detached
        self.node.left = None
        self.node.right = None
        self.node.parent = None

    def revert(self):
        right_child = self.propagation_order.get()

        # Set original node back in tree position
        if self.is_root:
            dangling_child = self.tree.root
            self.tree.root = self.node
        else:
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
        dangling_child.parent = self.node

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
    def __init__(self, tree, node: Node, parent: Optional['Node'], insert_left: bool):
        super().__init__(tree)
        self.node = node
        self.parent = parent
        self.insert_left = insert_left

    def do(self):
        if self.parent is None:
            if self.insert_left:
                self.node.left = self.tree.root
                self.tree.root = self.node
                self.node.left.parent = self.node
            else:
                self.node.right = self.tree.root
                self.tree.root = self.node
                self.node.right.parent = self.node
        elif self.insert_left:
            if self.parent.has_left_child():
                old_child = self.parent.left
                self.parent.replace_child(old_child, self.node)
                self.node.parent = self.parent
                self.node.left = old_child
            else:
                self.parent.left = self.node
                self.node.parent = self.parent
        else:
            if self.parent.has_right_child():
                old_child = self.parent.right
                self.parent.replace_child(old_child, self.node)
                self.node.parent = self.parent
                self.node.right = old_child
            else:
                self.parent.right = self.node
                self.node.parent = self.parent

    def revert(self):
        if self.parent is None:
            if self.insert_left:
                self.tree.root = self.node.left
                self.node.left = None
                self.node.left.parent = None
            else:
                self.tree.root = self.node.right
                self.node.right = None
                self.node.left.parent = None
        if self.insert_left:
            if self.node.has_left_child():
                old_child = self.node.left
                self.parent.replace_child(self.node, old_child)
                self.node.parent = None
                self.node.left = None
            else:
                self.parent.left = None
                self.node.parent = None
        else:
            if self.node.has_right_child():
                old_child = self.node.right
                self.parent.replace_child(self.node, old_child)
                self.node.parent = None
                self.node.right = None
            else:
                self.parent.right = None
                self.node.parent = None
