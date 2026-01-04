"""
Implement the function that meets the specifications below
"""

def sum_str_lengths(L):
    """
    L is a non-empty list containing either: 
    * string elements or 
    * a non-empty sublist of string elements
    Returns the sum of the length of all strings in L and 
    lengths of strings in the sublists of L. If L contains an 
    element that is not a string or a list, or L's sublists 
    contain an element that is not a string, raise a ValueError.
    """
    # Your code here
    total:int = 0
    for element in L:
        if isinstance(element,str):
            total += len(element)
        elif isinstance(element,list):
            for e in element:
                if isinstance(e,str):
                    total += len(e)
                else:
                    raise ValueError
        else:
            raise ValueError
    return total

# Examples:
print(sum_str_lengths(["abcd", ["e", "fg"]]))  # prints 7
print(sum_str_lengths([12, ["e", "fg"]]))      # raises ValueError
print(sum_str_lengths(["abcd", [3, "fg"]]))    # raises ValueError
