"""
Assume you are given an integer 0<=N<=1000.
Write a piece of Python code that uses bisection search to guess N.
The code prints two lines: count: with how many guesses it took to
find N, and answer: with the value of N. Hints: If the halfway value
is exactly in between two integers, choose the smaller one.
"""

#Assumed number N given
N = 47

#Beginning of Finger Exercise

def bisection(start, end, N, count):
    mid = int((start + end)//2)
    new_count = count + 1
    if mid == N:
        return new_count, mid
    elif mid < N:
        return bisection(mid, end, N, new_count)
    elif mid > N:
        return bisection(start, mid, N, new_count)

print(bisection(0,1000,N,0))
