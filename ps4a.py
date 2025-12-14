def get_permutations(sequence:str) -> list[str]:
    if len(sequence) == 1:
        return [sequence]
    first_char:str = sequence[0]
    rest_permutations:list[str] = get_permutations(sequence[1:])
    result:list[str] = []
    for perm in rest_permutations:
        for i in range(len(perm) + 1):
            new_perm:str = perm[:i] + first_char + perm[i:]
            result.append(new_perm)
    return result

if __name__ == '__main__':
   #EXAMPLE
   example_input = 'cat'
   print('Input:', example_input)
   print('Output:', get_permutations(example_input))
