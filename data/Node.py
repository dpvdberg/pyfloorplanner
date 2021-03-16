from typing import Optional

from data.Module import Module

node_id = 0


def reset_node_id():
    global node_id
    node_id = 0


class Node:
    def __init__(self, value: Module,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None,
                 parent: Optional['Node'] = None):
        self.value: Module = value
        self.left: Optional['Node'] = left
        self.right: Optional['Node'] = right
        self.parent: Optional['Node'] = parent
        self.rotated: bool = False

        # Only used for illustrating purposes
        global node_id
        self.id = node_id
        node_id = node_id + 1

    def is_leaf(self) -> bool:
        return not self.has_left_child() and not self.has_right_child()

    def has_two_children(self) -> bool:
        return self.has_left_child() and self.has_right_child()

    def has_right_child(self) -> bool:
        return self.right is not None

    def has_left_child(self) -> bool:
        return self.left is not None

    def get_first_child(self) -> Optional['Node']:
        if self.left is not None:
            return self.left
        elif self.right is not None:
            return self.right
        else:
            return None

    def replace_child(self, old: 'Node', new: 'Node') -> bool:
        '''
        Replaces the old child with a new child and returns whether the old child was right
        :param old: Old child
        :param new: New child
        :return: Whether the old child was on the right
        '''
        if self.left is old:
            self.left = new
            return False
        elif self.right is old:
            self.right = new
            return True
        else:
            raise Exception("Could not find node to be replaced in children")

    def has_child(self, node: 'Node'):
        return self.left is node or self.right is node

    def __str__(self):
        return str(self.id)
