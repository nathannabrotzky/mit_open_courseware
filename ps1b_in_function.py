def part_b(yearly_salary, portion_saved, cost_of_dream_home, semi_annual_raise):
	#########################################################################
	
	portion_down_payment:float = 0.25
	down_payment:float = cost_of_dream_home * portion_down_payment
	amount_saved:float = 0
	r:float = 0.05
	
	###############################################################################################
	## Determine how many months it would take to get the down payment for your dream home below ## 
	###############################################################################################
	
	# This is a recursive approach to the problem
	def time_helper(amount_saved:float,
	                portion:float,
	                down_payment:float,
	                salary:float,
	                salary_raise:float,
	                rate:float,
	                month:int) -> int:
	    monthly_salary:float = salary / 12.0
	    if amount_saved >= down_payment:
	        return month
	    else:
	        amount_saved += monthly_salary * portion + amount_saved * (rate / 12)
	        month += 1
	        if month % 6 == 0:
	            salary *= (1 + salary_raise)
	        return time_helper(amount_saved,
	                           portion,
	                           down_payment,
	                           salary,
	                           salary_raise,
	                           rate,
	                           month)
	    
	start_month:int = 0
	months:int = time_helper(amount_saved,
	                     portion_saved,
	                     down_payment,
	                     yearly_salary,
	                     semi_annual_raise,
	                     r,
	                     start_month)
	
	print(f"Number of months: {months}")
	return months