"""
Write a program that asks the user to enter an integer and prints
two integers, root and pwr, such that 0 < pwr < 6 and root**pwr is
equal to the integer entered by the user. If no such pair of integers
exists, it should print a message to that effect.
"""

user_int = int(input("Enter an integer: "))

#Exhaustive method; check and print all combinations
check = 0
for root in range(user_int+1):
    for power in range(7):
        if root**power == user_int:
            print(root, power)
            check += 1
if check == 0:
    print("No such pairs of integers exist")
