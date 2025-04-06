import itertools
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
    # build AVLTree using a preorder list (with None values)
    def __init__(self, preorder = None):
        if not preorder:
            self.root = None
            return

        dummy = TreeNode()
        # second value is True if left is the next to insert to, False if inserting
        # to right
        queue = deque()
        queue.append([dummy, False])
        for val in preorder:

            if val is not None:
                node = TreeNode(val)
                queue.append([node, True])
            else:
                node = None

            parent, left = queue[0]
            if left:
                parent.left = node
                queue[0][1] = False
            else:
                parent.right = node
                queue.popleft()

        self.root = dummy.right


    def __str__(self):
        layers = self.get_layers()

        width = len(layers[-1])
        locations = [[] for _ in range(len(layers))]

        # create print locations of the bottom of the tree
        for i in range(width):
            # +1 for an added space
            locations[-1].append(i * (NODE_WIDTH + 1))

        for j in range(len(locations)-2, -1, -1):
            for a, b in itertools.batched(locations[j+1], 2):
                # each parent is in the center of its two children
                locations[j].append((a+b)//2)

        output_li: list = []
        # layers[i][j] is stored at locations[i][j]
        for i in range(len(layers)):
            # print dashes if not the first layer
            if i > 0:
                prev = 0
                forward_slash = True
                for val, location in zip(layers[i], locations[i]):
                    output_li.append(" " * (location - prev))
                    if val != '':
                        if forward_slash:
                            output_li.append(format('/', f' ^{NODE_WIDTH}'))
                        else:
                            output_li.append(format('\\', f' ^{NODE_WIDTH}'))
                    else:
                        output_li.append(' ' * NODE_WIDTH)

                    prev = location + NODE_WIDTH
                    forward_slash = not forward_slash
                output_li.append('\n')

            prev = 0
            for val, location in zip(layers[i], locations[i]):
                output_li.append(" " * (location - prev))
                output_li.append(format(val, f' ^{NODE_WIDTH}'))
                prev = location + NODE_WIDTH
            output_li.append('\n')

        return ''.join(output_li)


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