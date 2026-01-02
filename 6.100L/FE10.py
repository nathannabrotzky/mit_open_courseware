"""
Implement the function that meets the specifications below
"""

def all_true(n:int, Lf:list) -> bool:
    """ n is an int
        Lf is a list of functions that take in an int and return a Boolean
    Returns True if each and every function in Lf returns True when called 
    with n as a parameter. Otherwise returns False. 
    """
    # Your code here
    flag:bool = True
    for f in Lf:
        if not f(n):
            flag:bool = False
            break
    return flag

# Examples:    
all_true() # prints 6
