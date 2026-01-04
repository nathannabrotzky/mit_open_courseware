def dp_make_weight(egg_weights:tuple[int], target_weight:int, memo:dict[int,int] = {}) -> int:
    if target_weight == 1:
        return 1
    if target_weight in memo:
        return memo[target_weight]
    min_eggs = float('inf')
    reversed_eggs = egg_weights[::-1]
    for weight in reversed_eggs:
        if weight <= target_weight:
            num_eggs = 1 + dp_make_weight(egg_weights, target_weight - weight, memo)
            if num_eggs < min_eggs:
                min_eggs = num_eggs
    memo[target_weight] = min_eggs
    return min_eggs

if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
