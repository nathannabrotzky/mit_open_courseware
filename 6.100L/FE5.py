"""
Assume you are given a string variable named my_str. Write a
piece of Python code that prints out a new string containing
the even indexed characters of my_str. For example, if
my_str = "abcdefg" then your code should print out aceg.
"""

#Assumed given string variable
my_str = "abcdefg"

#Beginning of finger exercise
result = ""
for i, c in enumerate(my_str):
    result += c if i % 2 == 0 else ""
print(result)
