from collections import deque

from AVLTree import AVLTree

tree = AVLTree()
for i in range(1, 16):
    tree.insert(i)
    print(f"added {i: 2}: ", *(n for n in tree))

for i in range(1, 16):
    tree.discard(i)
    print(f"removed {i: 2}:", *(n for n in tree))



q = deque()
q.append(tree.root)
while q:
    for _ in range(len(q)):
        node = q.popleft()
        print(node.val, node.height, end=' ', sep=';')
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    print()
