class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 0

    def __repr__(self):
        return f"Node(val={self.val}, height={self.height})"

class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def get_height(node):
        return node.height if node else -1

    def balance_factor(self, node):
        return self.get_height(node.right) - self.get_height(node.left)

    def update_node(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self.update_node(node)
        self.update_node(right_child)
        return right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self.update_node(node)
        self.update_node(left_child)
        return left_child

    def balance(self, root):
        self.update_node(root)
        if self.balance_factor(root) > 1:
            if self.balance_factor(root.right) >= 0:
                return self.rotate_left(root)
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        elif self.balance_factor(root) < -1:
            if self.balance_factor(root.left) <= 0:
                return self.rotate_right(root)
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        return root

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, root, val):
        if not root:
            return Node(val)
        if val < root.val:
            root.left = self._insert(root.left, val)
        else:
            root.right = self._insert(root.right, val)
        return self.balance(root)

    def __iter__(self):
        yield from self.inorder(self.root)

    def inorder(self, root):
        if not root:
            return
        yield from self.inorder(root.left)
        yield root.val
        yield from self.inorder(root.right)