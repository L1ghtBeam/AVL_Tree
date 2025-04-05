class TreeNode:
    def __init__(self, val = None):
        self.val = val
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def __str__(self):
        layers = []
        # bfs to get all nodes in each layer
