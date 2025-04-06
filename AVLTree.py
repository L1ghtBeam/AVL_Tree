from collections import deque

NODE_WIDTH = 3

class TreeNode:
    def __init__(self, val = None):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.val)


class AVLTree:
    def __init__(self):
        self.root = None

    def __str__(self):
        layers = self.get_layers()

        tree_width = len(layers[-1])



    def get_layers(self) -> list[list[str]]:
        # 2D array of node values
        layers = []
        # bfs to get all nodes in each layer
        queue = deque()
        queue.append(self.root)
        nodes_remaining = True
        while nodes_remaining:
            layers.append([])
            nodes_remaining = False
            for _ in range(len(queue)):
                node = queue.popleft()
                if node:
                    layers[-1].append(str(node))
                    queue.append(node.left)
                    queue.append(node.right)
                    nodes_remaining = True
                else:
                    layers[-1].append('')
                    queue.append(None)
                    queue.append(None)
        # remove last layer of all None
        layers.pop()

        return layers