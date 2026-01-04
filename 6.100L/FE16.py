"""
Implement the function that meets the specifications below
"""

def flatten(L:list[int|list]) ->list[int]:
    """ 
    L: a list 
    Returns a copy of L, which is a flattened version of L 
    """
    # Your code here
    def flat_helper(L:list[int|list], new_L:list[int]):
        for element in L:
            if isinstance(element,int):
                new_L.append(element)
            else:
                flat_helper(element,new_L)
    new_L:list[int] = []
    flat_helper(L, new_L)
    return new_L
        
# Examples:
L = [[1,4,[6],2],[[[3]],2],4,5]
print(flatten(L)) # prints the list [1,4,6,2,3,2,4,5]
