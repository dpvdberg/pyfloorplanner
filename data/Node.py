from typing import Optional, List

from data.Module import Module

node_id = 0


def reset_node_id():
    global node_id
    node_id = 0


class Node:
    def __init__(self, value: Module,
                 left: Optional['Node'] = None,
                 right: Optional['Node'] = None,
                 parent: Optional['Node'] = None,
                 id: Optional[int] = None,
                 rotated : bool = False):
        self.value: Module = value
        self.left: Optional['Node'] = left
        self.right: Optional['Node'] = right
        self.parent: Optional['Node'] = parent
        self.rotated: bool = rotated

        # Only used for illustrating purposes
        global node_id
        if id is None:
            self.id = node_id
            node_id = node_id + 1
        else:
            self.id = id

    def clone(self, parent: Optional['Node'] = None) -> 'Node':
        clone = Node(
            self.value,
            None,  # left
            None,  # right
            None,  # parent
            self.id,
            self.rotated
        )
        clone.left = self.left.clone(clone) if self.left is not None else None
        clone.right = self.right.clone(clone) if self.right is not None else None
        clone.parent = parent
        return clone

    def nodes_in_subtree(self) -> List['Node']:
        descendants = [self]
        if self.has_left_child():
            descendants.extend(self.left.nodes_in_subtree())
        if self.has_right_child():
            descendants.extend(self.right.nodes_in_subtree())
        return descendants

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

    def replace_child(self, old: 'Node', new: Optional['Node']) -> bool:
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

    def validate_parents(self, parent: Optional['Node'] = None) -> bool:
        valid = self.parent is parent
        valid = valid and (self.right is None or self.right.validate_parents(self))
        valid = valid and (self.left is None or self.left.validate_parents(self))
        return valid
