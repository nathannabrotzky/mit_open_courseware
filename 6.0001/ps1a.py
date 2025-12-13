annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

portion_down_payment = 0.25
current_savings = 0
r = 0.04
monthly_salary = annual_salary/12

return_month = 0
break_value = total_cost * portion_down_payment

while (current_savings < break_value):
    return_month += 1
    current_savings += current_savings*r/12
    current_savings += monthly_salary*portion_saved

print(f"Number of months: {return_month}")
