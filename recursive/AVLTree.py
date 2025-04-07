from typing import Any, Generator
from collections.abc import MutableSet

class Node:
    def __init__(self, val):
        self.val: Any = val
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = 0
        self.size: int = 1

    def __repr__(self):
        return f"Node(val={self.val}, height={self.height})"

class AVLTree(MutableSet):
    def __init__(self):
        self.root: Node | None = None

    def __len__(self) -> int:
        if not self.root:
            return 0
        return self.root.size

    @staticmethod
    def get_height(node: Node | None) -> int:
        return node.height if node else -1

    @staticmethod
    def get_size(node: Node | None) -> int:
        return node.size if node else 0

    def balance_factor(self, node: Node) -> int:
        return self.get_height(node.right) - self.get_height(node.left)

    def update_node(self, node: Node) -> None:
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        node.size = 1 + self.get_size(node.left) + self.get_size(node.right)

    def rotate_left(self, node: Node) -> Node:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self.update_node(node)
        self.update_node(right_child)
        return right_child

    def rotate_right(self, node: Node) -> Node:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self.update_node(node)
        self.update_node(left_child)
        return left_child

    def balance(self, root: Node) -> Node:
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

    def add(self, val: Any):
        self.root = self._add(self.root, val)

    def _add(self, root: Node | None, val: Any) -> Node:
        if not root:
            return Node(val)
        if val < root.val:
            root.left = self._add(root.left, val)
        else:
            root.right = self._add(root.right, val)
        return self.balance(root)

    def __iter__(self):
        yield from self.inorder(self.root)

    def inorder(self, root: Node | None) -> Generator[Any, None, None]:
        if not root:
            return
        yield from self.inorder(root.left)
        yield root.val
        yield from self.inorder(root.right)

    def discard(self, val: Any) -> None:
        self.root = self._discard(self.root, val)

    def _discard(self, root: Node | None, val: Any) -> Node | None:
        if not root:
            return None
        if root.val == val:
            if root.left:
                predecessor = self.predecessor(root)
                root.val, predecessor.val = predecessor.val, root.val
                root.left = self._discard(root.left, val)
            elif root.right:
                successor = self.successor(root)
                root.val, successor.val = successor.val, root.val
                root.right = self._discard(root.right, val)
            else:
                return None
        elif val < root.val:
            root.left = self._discard(root.left, val)
        else:
            root.right = self._discard(root.right, val)
        return self.balance(root)

    @staticmethod
    def predecessor(root: Node) -> Node | None:
        if not root.left:
            return None
        root = root.left
        while root.right:
            root = root.right
        return root

    @staticmethod
    def successor(root: Node) -> Node | None:
        if not root.right:
            return None
        root = root.right
        while root.left:
            root = root.left
        return root

    def __contains__(self, x):
        node = self.root
        while node:
            if node.val == x:
                return True
            if x < node.val:
                node = node.left
            else:
                node = node.right
        return False

    def median(self) -> Any:
        if not self.root:
            raise RuntimeError("Cannot find median of an empty tree")
        if self.root.size % 2 == 1:
            return self.find_median(0)
        return (self.find_median(-1) + self.find_median(1)) / 2

    def find_median(self, target: Any) -> Any:
        """Find the value where the length of its right subtree minus its left subtree is the target"""
        node = self.root
        left = self.get_size(node.left)
        right = self.get_size(node.right)
        balance = right - left
        while balance != target:
            if balance > target:
                right -= self.get_size(node.right)
                node = node.right
                left += 1 + self.get_size(node.left)
                right += self.get_size(node.right)
            else:
                left -= self.get_size(node.left)
                node = node.left
                right += 1 + self.get_size(node.right)
                left += self.get_size(node.left)
            balance = right - left
        return node.val