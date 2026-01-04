"""
Write a program that asks the user to input 10 integers, and then
prints the largest odd number that was entered. If no odd number was entered, it
should print a message to that effect.
"""

counter:int = 0
max_odd:int|None = None

while counter < 10:
    number:int = int(input("Enter an integer: "))
    if number % 2 == 1 and (max_odd is None or number > max_odd):
        max_odd:int|None = number
    counter += 1

if max_odd is None:
    print("No odd number was entered")
else:
    print(f"Largest odd number: {max_odd}")
