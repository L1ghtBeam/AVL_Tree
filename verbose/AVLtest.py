from AVLTree import AVLTree


# preorder = ['E', 'C', 'F', 'B', 'D', None, None, 'A']
# tree = AVLTree(preorder)
# print(tree)
#
# print(f"{'D' in preorder = }\n{'G' in preorder = }",end='\n\n')
#
# print(*(item for item in tree))
#
# preorder2 = [i for i in range(1, 16)]
# tree2 = AVLTree(preorder2)
# print(tree2)
#

tree = AVLTree()
for i in range(1, 8):
    tree.add(i)
    print(f"=== Tree after inserting {i} ===", tree, sep='\n')


tree = AVLTree()
for i in range(7, 0, -1):
    tree.add(i)
    print(f"=== Tree after inserting {i} ===", tree, sep='\n')


print("\n Balancing worst case list:")

preorder_line = ['A', None, 'B', None, 'C', None, 'D', None, 'E', None, 'F']
tree_line = AVLTree(preorder_line)
print(tree_line)

tree_line.add('G')
print(tree_line)