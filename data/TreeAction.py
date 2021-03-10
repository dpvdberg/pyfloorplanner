from data.Tree import Tree


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
    def __init__(self, tree, node):
        super().__init__(tree)
        self.node = node
        self.orig_parent = node.parent

    def do(self):
        #TODO: delete and insert in random new place
        pass

    def revert(self):
        self.tree.delete(self.node)
        self.tree.insert(self.node, self.orig_parent)

