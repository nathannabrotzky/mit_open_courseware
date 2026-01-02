"""
Implement the function that meets the specifications below
"""

def count_sqrts(nums_list:list[int]) -> int:
    """
    nums_list: a list
    Assumes that nums_list only contains positive numbers and that there
    are no duplicates.
    Returns how many elements in nums_list are exact squares of elements
    in the same list, including itself.
    """
    # Your code here
    total:int = 0
    for num in nums_list:
        if num**2 in nums_list:
            total += 1
    return total

# Examples:    
print(count_sqrts([3,4,2,1,9,25])) # prints 3
