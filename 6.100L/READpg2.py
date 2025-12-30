"""
From Reading 1, 2.1-2.2
Heron's Method (or Babylonian Method)
For approximating square roots

Example of a guess-and-check algorithm
Make initial guess g
Compare g*g to x
If too different, average g and x/g into new g
Repeat comparison and averaging of g*g to x
"""

def heron_sqrt(x:float|int) -> float:
    if not (isinstance(x, float) or isinstance(x, int)):
        print("Invalid input number")
        return -1
    if x < 0:
        print("Invalid input number")
        return -1
    initial_guess:int = len(str(x)) * 5 #arbitrary starting point
    def heron_helper(guess):
        if abs(x - (guess * guess)) < 0.0001: #precision set to 4
            return guess
        else:
            new_guess:float = (guess + (float(x) / guess)) / 2
            return heron_helper(new_guess)
    result:float = heron_helper(initial_guess)
    return round(result,4)

number:int = 25
print(heron_sqrt(number))
