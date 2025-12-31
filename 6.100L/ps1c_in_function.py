def part_c(initial_deposit):
	#########################################################################
	
	months:int = 36
	cost_of_house:int = 800000
	portion_down_payment:float = 0.25
	down_payment:float = cost_of_house * portion_down_payment
	
	##################################################################################################
	## Determine the lowest rate of return needed to get the down payment for your dream home below ##
	##################################################################################################
	
	def rate_helper(pv:float,
	                fv:float,
	                t:int,
	                rates:tuple[float],
	                start:int,
	                end:int,
	                steps:int):
	    def amount_saved(pv:float, t:int, r:float):
	        return pv * ((1 + (r / 12))**t)
	    if amount_saved(pv, t, 1) < (fv-100):
	        return None, steps
	    mid:int = int((end + start) // 2)
	    new_rate:float = rates[mid]/10000.0
	    amount:float = amount_saved(pv, t, new_rate)
	    if (fv-100) < amount < (fv+100):
	        return new_rate, steps
	    else:
	        new_start:int = start if amount > (fv+100) else mid
	        new_end:int = end if amount < (fv-100) else mid
	        return rate_helper(pv, fv, t, rates, new_start, new_end, steps + 1) 
	
	rates:tuple[float] = range(10000)
	steps:int = 0
	start:int = 0
	end:int = 10000 - 1
	
	r, steps = rate_helper(initial_deposit,
	                       down_payment,
	                       months,
	                       rates,
	                       start,
	                       end,
	                       steps)
	
	print(f"Best savings rate: {r}")
	
	print(f"Steps in bisection search: {steps}")
	return r, steps
