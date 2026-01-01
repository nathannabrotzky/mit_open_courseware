#Binary search for the square root
x = 24
epsilon = 0.01
numGuesses = 0
low = 0.0
high = max(1.0, x)
ans = (high + low)/2.0
while abs(ans**2 - x) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    numGuesses += 1
    if ans**2 < x:
        low = ans
    else:
        high = ans
    ans = (high + low)/2.0
print('numGuesses =', numGuesses)
print('Square root of', x, 'is about', ans)

#Newton-Raphson for square root
#Find x such that x**2 - 24 is within epsilon of 0
epsilon = 0.01
k = 24.0
guess = k/2.0
numGuesses = 0
while abs(guess*guess - k) >= epsilon:
    print("guess =", guess)
    numGuesses += 1
    guess = guess - (((guess**2) - k)/(2*guess))
print('numGuesses =', numGuesses)
print('Square root of', k, 'is about', guess)
