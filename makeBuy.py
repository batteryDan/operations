import numpy_financial as npf
import matplotlib.pyplot as plt
import pandas as pd

# Parameters
purchase_cost = 4895000  # Purchase of a facility
down_payment = 0.20 * purchase_cost  # 20% down payment
loan_amount = purchase_cost - down_payment  # Amount financed
interest_rate = 0.05  # 5% annual interest rate
loan_term_years = 30  # 30-year fixed mortgage
monthly_interest_rate = interest_rate / 12  # Monthly interest rate
num_payments = loan_term_years * 12  # Total number of payments

# Monthly mortgage payment using the formula for fixed-rate mortgages
monthly_mortgage_payment = npf.pmt(monthly_interest_rate, num_payments, -loan_amount)

yearly_bom_cost = 90000 * 20  # Yearly BOM costs
monthly_opex = 120 * 7 * 2080 / 12 + purchase_cost*0.01/12 # Monthly operating expenses + property taxes california
monthly_income = 600000  # Actual monthly income

# Time period for analysis (10 years)
max_months = 5 * 12

# Discount rate sweep from 0% to 20% at 2% intervals
discount_rates = [i / 100 for i in range(0, 21, 2)]

# Prepare the plot
plt.figure(figsize=(14, 8))

# Loop over each discount rate
for rate in discount_rates:
    monthly_discount_rate = rate / 12
    total_npvs = []

    # Initial cash flow (down payment + first year's BOM)
    initial_cash_flow = -down_payment - yearly_bom_cost
    
    # Calculate NPVs for each month up to 10 years
    for months in range(1, max_months + 1):
        if months <= 12:
            # First 12 months with no income, only expenses and mortgage payments
            cash_flows = [initial_cash_flow] + [-(monthly_opex + monthly_mortgage_payment)] * months
        else:
            # After 12 months, income starts along with ongoing expenses and mortgage payments
            cash_flows = [initial_cash_flow] + [-(monthly_opex + monthly_mortgage_payment)] * 12 + [(monthly_income - monthly_opex - monthly_mortgage_payment)] * (months - 12)

        # Calculate NPV
        npv = npf.npv(monthly_discount_rate, cash_flows)
        total_npvs.append(npv)

    # Create a DataFrame to visualize the NPV values
    npv_data = pd.DataFrame({
        'Month': range(1, max_months + 1),
        'NPV': total_npvs,
    })

    # Plot NPV over time for this discount rate
    plt.plot(npv_data['Month'], npv_data['NPV'], label=f'NPV (r={rate*100:.0f}%)', linestyle='-', marker='o', markersize=3)

plt.title('NPV over Time at Varying Discount Rates with 12-Month Revenue Delay and Mortgage Financing')
plt.xlabel('Months')
plt.ylabel('NPV ($)')
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='', linewidth=0)
plt.tick_params(axis='both', which='both', length=5, width=1)
plt.tight_layout()
plt.show()
