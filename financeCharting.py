import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.dates import MonthLocator, DateFormatter

# Data
data = {
    'Date': [
        '2024-06-01', '2024-07-01', '2024-08-01', '2024-09-01', '2024-10-01', '2024-11-01', '2024-12-01',
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', 
        '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01', '2025-12-01', '2026-01-01', '2026-02-01', 
        '2026-03-01', '2026-04-01', '2026-05-01', '2026-06-01', '2026-07-01', '2026-08-01', '2026-09-01', 
        '2026-10-01', '2026-11-01', '2026-12-01', '2027-01-01', '2027-02-01', '2027-03-01', '2027-04-01', 
        '2027-05-01', '2027-06-01', '2027-07-01', '2027-08-01', '2027-09-01', '2027-10-01', '2027-11-01', 
        '2027-12-01'
    ],
    'Value': [
        -124800, -549600, -974400, -1099200, -1565600, -2715200, 1985200, 1673200, 1257200, 1737200,
        16593200, 13705200, 11028200, 37942200, 41552200, 28258200, 9715200, 18368200, -382800, -4777800,
        9623200, -9544800, 5863200, 18523200, 28425200, 39528200, 50527200, 98887200, 19255200, 39415200,
        109108200, 145100200, 180676200, 260271200, 301180200, 341673200, 381195200, 456771200, 495461200, 
        587215200, 645863200, 704095200, 765061200
    ]
}

# Convert date strings to datetime objects
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Convert dates to numerical values for fitting
df['Time'] = (df['Date'] - df['Date'].min()).dt.days

# Define the power function to fit: y = a * x^b
def power_func(x, a, b):
    return a * np.power(x, b)

# Fit the data
popt, pcov = curve_fit(power_func, df['Time'], df['Value'], maxfev=10000)

# Generate fitted values
df['Fitted'] = power_func(df['Time'], *popt)

# Convert values to million USD for y-axis
df['Value_MUSD'] = df['Value'] / 1e6
df['Fitted_MUSD'] = df['Fitted'] / 1e6

# Plot the results
plt.figure(figsize=(12, 6))

# Plot original data and fitted curve
# plt.plot(df['Date'], df['Value_MUSD'], label='Original Data', marker='o')
plt.plot(df['Date'], df['Fitted_MUSD'], label=f'Power Fit: y = {popt[0]:.2e} * x^{popt[1]:.2f}', color='orange')

# Formatting
plt.xlabel('Date', fontname='Arial')
plt.ylabel('Value (MUSD)', fontname='Arial')

# Set quarter-based x-axis ticks with quarter labels
quarterly_locator = MonthLocator(interval=3)
quarterly_formatter = DateFormatter('%b %Y')
plt.gca().xaxis.set_major_locator(quarterly_locator)
plt.gca().xaxis.set_major_formatter(quarterly_formatter)

# Adding Q1, Q2, etc. labels manually
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
for i, (date, label) in enumerate(zip(pd.date_range(start='2025-01-01', end='2027-12-01', freq='QS'), quarters * 8)):
    plt.text(date, df['Value_MUSD'].max() * 0.9, label, ha='center', fontsize=8, color='gray', fontname='Arial')

# Remove plot border (spines)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Display legend without grid lines
plt.legend(prop={'family': 'Arial'})
plt.tight_layout()
plt.show()
