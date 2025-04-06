from AVLTree import AVLTree


preorder = ['A', 'B', 'C', 'D', 'E', None, None, 'F']
tree = AVLTree(preorder)
print(tree)

preorder2 = [i for i in range(1, 16)]
tree2 = AVLTree(preorder2)
print(tree2)