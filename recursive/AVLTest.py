from collections import deque

from AVLTree import AVLTree

def main():
    tree = AVLTree()
    for i in range(1, 16):
        tree.add(i)
        print(f"added {i: 2}: ", *(n for n in tree))
        print("median:", tree.median())
        if tree.median() != median(tree):
            print(f"Warning! Median should be {median(tree)}")

    print("Size of root:", len(tree))
    print(f"{4 in tree = }\n{18 in tree = }")

    for i in range(2, 15):
        tree.discard(i)
        print(f"removed {i: 2}:", *(n for n in tree))
        print("median:", tree.median())
        if tree.median() != median(tree):
            print(f"Warning! Median should be {median(tree)}")

    print("Size of root:", tree.root.size)

    if tree.root is not None:
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

def median(tree: AVLTree):
    inorder = [val for val in tree]
    if len(inorder) % 2 == 1:
        return inorder[len(inorder) // 2]

    return (inorder[len(inorder) // 2 - 1] + inorder[len(inorder) // 2]) / 2

main()