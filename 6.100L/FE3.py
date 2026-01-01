"""
Assume you are given a positive integer variable named N.
Write a piece of Python code that prints hello world on separate lines,
N times. You can use either a while loop or a for loop.
"""

#Assumed value N used for implementation
N = 5

#Beginning of Finger Exercise
for i in range(N):
    print("hello world")

#ideally, I would avoid using a loop for this and use string functions
print("\n".join(("hello world",)*N))
