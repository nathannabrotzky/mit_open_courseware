#Bisection Search/Binary Search

starting_salary = float(input("Enter the starting salary: "))

semi_annual_raise = 0.07
annual_return = 0.04
down_payment = 0.25
total_cost = 1000000
target_month = 36
break_value = total_cost * down_payment

values = list(range(1,10001))
left = 0
right = len(values) - 1
steps = 0
while ((right - left) > 1):
    monthly_salary = starting_salary / 12.0
    mid = (right + left) / 2
    test_val = values[int(mid)]
    current_savings = 0
    portion_saved = test_val/10000.0
    for i in range(target_month):
        current_savings += current_savings*annual_return/12
        current_savings += monthly_salary*portion_saved
        if (i + 1) % 6 == 0:
            monthly_salary = monthly_salary * (1 + semi_annual_raise)
    if current_savings < break_value:
        left = mid
    else:
        right = mid
    steps += 1

if current_savings < break_value and right == len(values) - 1:
    print("It is not possible to pay the down payment in three years.")
else:
    print(f"Best savings rate: {portion_saved}")
    print(f"Steps in bisection search: {steps}")
