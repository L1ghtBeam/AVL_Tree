import itertools
from collections import deque
from collections.abc import MutableSet

NODE_WIDTH = 3

class TreeNode:
    def __init__(self, val = None):
        self.val = val
        self.left = None
        self.right = None
        self.height = 0

    def __str__(self):
        return str(self.val)


class AVLTree(MutableSet):
    # build AVLTree using a preorder list (with None values)
    def __init__(self, preorder: list = None):
        self.length = 0
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
                self.length += 1
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


    def __contains__(self, val):
        if not self.root:
            return False
        node = self.root
        while node:
            if node.val == val:
                return True
            if node.val < val:
                node = node.left
            else:
                node = node.right

        return False


    # use inorder traversal as the iterator
    def __iter__(self):
        if not self.root:
            return
        stack = []
        node = self.root
        while stack or node:
            # traverse left, remembering visited nodes
            while node:
                stack.append(node)
                node = node.left
            # get latest visited node
            node = stack.pop()
            # inorder process
            yield node.val
            # traverse right
            node = node.right


    def add(self, val):
        new_node = TreeNode(val)
        self.length += 1
        if not self.root:
            self.root = new_node
            return
        stack, node = [], self.root
        while True:
            stack.append(node)
            if val < node.val:
                if node.left:
                    node = node.left
                else:
                    node.left = new_node
                    break
            else:
                if node.right:
                    node = node.right
                else:
                    node.right = new_node
                    break

        self.balance(stack)


    def discard(self, val):
        if not self.root:
            return

        stack, node = [], self.root
        while node and node.val != val:
            stack.append(node)
            if node.val < val:
                node = node.left
            else:
                node = node.right

        # node not in BST
        if not node:
            return

        # node must now be equal to the node we're looking for
        self.length -= 1

        # if is not leaf, then swap it downwards until it is
        while node.left or node.right:
            if node.left:
                swap_node = self.predecessor(node, stack)
            else:
                swap_node = self.successor(node, stack)
            node.val, swap_node.val = swap_node.val, node.val
            node = swap_node

        # remove from parent
        if stack[-1].left == node:
            stack[-1].left = None
        else:
            stack[-1].right = None

        self.balance(stack)


    def balance(self, stack: list[TreeNode]):
        for node in reversed(stack):
            # update height
            node.height = 1 + max(AVLTree.height(node.left), AVLTree.height(node.right))
            # check if this node requires balancing
            if abs(self.balance_factor(node)) <= 1:
                # if balance factor becomes 0, we can stop retracing
                if self.balance_factor(node) == 0:
                    return
                # otherwise, check the next node
                continue

            if self.balance_factor(node) > 1:
                # rotate right child
                right_child = node.right
                if self.balance_factor(right_child) >= 0:
                    self.rotate_left(node)
                else:
                    self.rotate_right_left(node)
            else:
                left_child = node.left
                if self.balance_factor(left_child) <= 0:
                    self.rotate_right(node)
                else:
                    self.rotate_left_right(node)


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

        # remove last newline for consistency with print()
        output_li.pop()
        return ''.join(output_li)


    def __len__(self):
        return self.length


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

    @staticmethod
    def predecessor(node: TreeNode, stack: list = None) -> TreeNode | None:
        """Return the predecessor of the node if it can be found in its subtree, otherwise return None
        :param node: node to begin the search from
        :param stack: optional stack to append all visited nodes to
        :return: a TreeNode if a predecessor was found, and None otherwise
        """
        if not node.left:
            return None
        node = node.left
        while node.right:
            if stack is not None:
                stack.append(node)
            node = node.right
        return node

    @staticmethod
    def successor(node: TreeNode, stack: list = None) -> TreeNode | None:
        """Return the successor of the node if it can be found in its subtree, otherwise return None
        :param node: node to begin the search from
        :param stack: optional stack to append all visited nodes to
        :return: a TreeNode if a successor was found, and None otherwise
        """
        if not node.right:
            return None
        node = node.right
        while node.left:
            if stack is not None:
                stack.append(node)
            node = node.left
        return node

    @staticmethod
    def height(node: TreeNode) -> int:
        return node.height if node else -1

    @staticmethod
    def balance_factor(node: TreeNode) -> int:
        return AVLTree.height(node.right) - AVLTree.height(node.left)

    @staticmethod
    def rotate_left(node):
        right_child = node.right
        # change which node is the root, to preserve parent pointer, do a swap of values and then swap children of node
        # to return the order
        node.val, right_child.val = right_child.val, node.val
        node.right, node.left = node.left, node.right

       # fix order of children
        right_child.left, right_child.right, node.right = node.right, right_child.left, right_child.right

        # update heights
        right_child.height = 1 + max(AVLTree.height(right_child.left), AVLTree.height(right_child.right))
        node.height = 1 + max(AVLTree.height(node.left), AVLTree.height(node.right))

    @staticmethod
    def rotate_right(node):
        left_child = node.left
        # change which node is the root, to preserve parent pointer, do a swap of values and then swap children of node
        # to return the order
        node.val, left_child.val = left_child.val, node.val
        node.right, node.left = node.left, node.right

        # fix order of children
        left_child.right, left_child.left, node.left = node.left, left_child.right, left_child.left

        # update heights
        left_child.height = 1 + max(AVLTree.height(left_child.left), AVLTree.height(left_child.right))
        node.height = 1 + max(AVLTree.height(node.left), AVLTree.height(node.right))

    @staticmethod
    def rotate_right_left(node):
        right_child = node.right
        AVLTree.rotate_right(right_child)
        AVLTree.rotate_left(node)

    @staticmethod
    def rotate_left_right(node):
        left_child = node.left
        AVLTree.rotate_left(left_child)
        AVLTree.rotate_right(node)

