"""
Assume you are given a positive integer variable named N.
Write a piece of Python code that finds the cube root of N.
The code prints the cube root if N is a perfect cube or it prints
error if N is not a perfect cube. Hint: use a loop that increments
a counter—you decide when the counter should stop.
"""

#Assumed positive integer N that is given
N = 8

#Beginning of finger exercise
check = 0
for i in range(N):
    if i**3 == N:
        print(i)
        break
    if i**3 > N:
        print("error")
        break
        
#could be handled recursively in function format
#check for positivity if not guaranteed positive integer N
