# Problem Set 4A
# Name: Nathan Nabrotzky
# Collaborators: None

from tree import Node # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the test named test_data_representation should pass.
tree1 = Node(8, Node(2, Node(1), Node(6)), Node(10))
tree2 = Node(7, Node(2, Node(1), Node(5, Node(3), Node(6))), Node(9, Node(8), Node(10)))
tree3 = Node(5, Node(3, Node(2), Node(4)), Node(14, Node(12), Node(21, Node(20), Node(26))))

def find_tree_height(tree:Node) -> int:
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    # TODO: Remove pass and write your code here
    right = tree.get_right_child()
    left = tree.get_left_child()
    if right is None and left is None:
        return 0
    elif right is None:
        return 1 + find_tree_height(left)
    elif left is None:
        return 1 + find_tree_height(right)
    else:
        return 1 + max(find_tree_height(left),find_tree_height(right))
    
def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree
        compare_func: a function that compares the child node value to the parent node value
            i.e. op(child_value,parent_value) for a max heap would return True if child_value < parent_value and False otherwise
                 op(child_value,parent_value) for a min meap would return True if child_value > parent_value and False otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    # TODO: Remove pass and write your code here
    right = tree.get_right_child()
    left = tree.get_left_child()
    if right is None and left is None:
        return True
    elif right is None and left is not None:
        return (compare_func(left.get_value(),tree.get_value())
                and is_heap(left, compare_func))
    elif left is None and right is not None:
        return (compare_func(right.get_value(),tree.get_value())
                and is_heap(right, compare_func))
    else:
        return (compare_func(right.get_value(),tree.get_value())
                and compare_func(left.get_value(),tree.get_value())
                and is_heap(right, compare_func)
                and is_heap(left, compare_func))

if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # IMPORTANT: Do not erase the pass statement below if you do not add your own code
    print(find_tree_height(tree1))
    print(find_tree_height(tree2))
    print(find_tree_height(tree3))
    pass
