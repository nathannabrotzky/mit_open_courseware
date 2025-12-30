"""
Write a program that examines three variables—x, y, and z—and
prints the largest odd number among them. If none of them are odd, it should
print a message to that effect.
"""

def largest_odd(x:int, y:int, z:int) -> int|None:
    if not (isinstance(x, int) and isinstance(y, int) and isinstance(z, int)):
        print("Invalid input: Expected all integers)
        return None
    largest_num:int|None = None
    if x % 2 == 1:
        largest_num:int|None = x
    if y % 2 == 1:
        largest_num:int|None = y if (largest_num is None or y > largest_num) else largest_num
    if z % 2 == 1:
        largest_num:int|None = z if (largest_num is None or z > largest_num) else largest_num
    if largest_num is None:
        print("No numbers were odd.")
    return largest_num

print(largest_odd(5,10,15))
    
