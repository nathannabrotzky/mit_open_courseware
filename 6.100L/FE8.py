"""
Implement the function that meets the specifications below
"""

def same_chars(s1, s2):
    """
    s1 and s2 are strings
    Returns boolean True is a character in s1 is also in s2, and vice 
    versa. If a character only exists in one of s1 or s2, returns False.
    """
    # Your code here
    chars = set(s1+s2)
    for c in chars:
        if c not in s1 or c not in s2:
            return False
    return True

# Examples:
print(same_chars("abc", "cab"))     # prints True
print(same_chars("abccc", "caaab")) # prints True
print(same_chars("abcd", "cabaa"))  # prints False
print(same_chars("abcabc", "cabz")) # prints False
