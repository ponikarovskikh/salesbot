# Given values for the new problem
monthly_payment = 500000  # in rubles
annual_interest_rate = 0.12
total_years = 10

# Monthly compounding
monthly_periods = total_years * 12
monthly_interest_rate = (1 + annual_interest_rate)**(1/12) - 1
print(monthly_interest_rate)
# Present value of an ordinary annuity (payments at the end of each period)
present_value_monthly = monthly_payment * (1 - (1 + monthly_interest_rate)**(-monthly_periods)) / monthly_interest_rate

print(present_value_monthly)