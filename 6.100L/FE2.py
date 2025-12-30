"""
Assume you are given a variable named number (has a numerical value).
Write a piece of Python code that prints out one of the following strings: 

positive if the variable number is positive
negative if the variable number is negative
zero if the variable number is equal to zero
"""

# Assumed this variable is given to us

number:int|float = 3.14159265

# Beginning of Finger Exercise part

if number > 0:
    print("positive")
elif number < 0:
    print("negative")
else:
    print("zero")
