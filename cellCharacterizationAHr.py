# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 14:01:06 2024
@author: DanielDomikaitis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Configuration settings
root_directory = r"C:\_git\inventory\testData"
voltage_range = np.round(np.arange(2.500, 3.601, 0.001), 3)  # Voltage range with 0.001V intervals
smoothing_window_size = 10  # Moving average window size for smoothing
sigma_multiplier = 1.1  # Sigma multiplier for voltage filtering

# Lists to store raw and processed data
all_datasets = []  # Store datasets and their statistics before filtering
max_capacities = []  # Store max capacities for statistics
dataset_mean_voltages = []  # Store mean voltages for statistics

def preprocess_dataset(file_path):
    """Preprocess the dataset with interpolation to 0.001V intervals."""
    df = pd.read_csv(file_path)

    print(f"\nLoaded data from: {file_path}")
    print(df[['Voltage (V)', 'Discharge Capacity (Ah)']].head())

    if 'Voltage (V)' not in df.columns or 'Discharge Capacity (Ah)' not in df.columns:
        raise ValueError("Required columns not found in dataset.")

    df_clean = df[['Voltage (V)', 'Discharge Capacity (Ah)']].dropna().sort_values(by='Voltage (V)')

    if df_clean.empty:
        print(f"Warning: {file_path} is empty after cleaning.")
        return None

    interpolated_capacity = np.interp(voltage_range, df_clean['Voltage (V)'], df_clean['Discharge Capacity (Ah)'])
    mean_voltage = df_clean['Voltage (V)'].mean()
    max_capacity = df_clean['Discharge Capacity (Ah)'].max()

    if max_capacity < 90:
        print(f"Dataset {file_path} has low max capacity: {max_capacity} Ah")

    return pd.DataFrame({'Voltage (V)': voltage_range, 'Discharge Capacity (Ah)': interpolated_capacity}), mean_voltage, max_capacity

# Process all datasets
for folder_name in os.listdir(root_directory):
    folder_path = os.path.join(root_directory, folder_name)

    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if "_Wb_" in file_name and file_name.endswith(".CSV"):
                file_path = os.path.join(folder_path, file_name)

                try:
                    result = preprocess_dataset(file_path)
                    if result is None:
                        continue

                    dataset, mean_voltage, max_capacity = result

                    all_datasets.append((dataset, mean_voltage, max_capacity))
                    dataset_mean_voltages.append(mean_voltage)

                    if max_capacity >= 90:
                        max_capacities.append(max_capacity)

                except Exception as e:
                    print(f"Failed to process {file_name}: {e}")

# Calculate voltage statistics for sigma-based filtering
mean_voltage_group = np.mean(dataset_mean_voltages)
std_voltage_group = np.std(dataset_mean_voltages)

lower_voltage_cutoff = mean_voltage_group - sigma_multiplier * std_voltage_group
upper_voltage_cutoff = mean_voltage_group + sigma_multiplier * std_voltage_group

# Filter datasets based on 90 Ah capacity and sigma voltage range
filtered_datasets = [
    dataset for dataset, mean_voltage, max_capacity in all_datasets
    if max_capacity >= 90 and lower_voltage_cutoff <= mean_voltage <= upper_voltage_cutoff
]

if not filtered_datasets:
    print("No datasets passed the filtering criteria.")
    exit()

# Calculate the average discharge capacity at each voltage step manually
average_discharge_capacity = np.zeros(len(voltage_range))

for voltage_index in range(len(voltage_range)):
    # Gather all discharge capacity values at this voltage step from each dataset
    capacities_at_voltage = [
        dataset.iloc[voltage_index]['Discharge Capacity (Ah)'] for dataset in filtered_datasets
    ]
    # Calculate the average for this voltage step
    average_discharge_capacity[voltage_index] = np.mean(capacities_at_voltage)

# Create a DataFrame for the average curve
average_capacity_curve = pd.DataFrame({'Voltage (V)': voltage_range, 'Discharge Capacity (Ah)': average_discharge_capacity})

# Apply smoothing to the average curve
average_capacity_curve['Discharge Capacity (Ah)'] = average_capacity_curve['Discharge Capacity (Ah)'].rolling(
    window=smoothing_window_size, center=True).mean()
average_capacity_curve.dropna(inplace=True)

# Export the average curve to CSV
output_csv_path = r"C:\_git\inventory\testData\average_capacity_curve.csv"
average_capacity_curve.to_csv(output_csv_path, index=False)
print(f"Average capacity curve exported to: {output_csv_path}")

# Plot 1: Histogram of max capacities with bell curve
mean_capacity = np.mean(max_capacities)
std_capacity = np.std(max_capacities)

plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(max_capacities, bins=30, alpha=0.7, color='gray', edgecolor='black')

bell_curve = norm.pdf(bins, mean_capacity, std_capacity)
plt.plot(bins, bell_curve * max(n), 'r--', linewidth=2)

plt.axvline(mean_capacity, color='blue', linestyle='dashed', linewidth=2, label=f'Mean: {mean_capacity:.2f} Ah')
plt.axvline(mean_capacity + 2 * std_capacity, color='green', linestyle='dashed', linewidth=1, label=f'+2σ')
plt.axvline(mean_capacity - 2 * std_capacity, color='green', linestyle='dashed', linewidth=1, label=f'-2σ')

plt.xlabel('Max Discharge Capacity (Ah)')
plt.ylabel('Frequency')
plt.title('Histogram of Max Discharge Capacities with Bell Curve')
plt.legend()
plt.grid(True)
plt.show()

# Plot 2: Histogram of dataset mean voltages with bell curve
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(dataset_mean_voltages, bins=30, alpha=0.7, color='gray', edgecolor='black')

bell_curve = norm.pdf(bins, mean_voltage_group, std_voltage_group)
plt.plot(bins, bell_curve * max(n), 'r--', linewidth=2)

plt.axvline(mean_voltage_group, color='blue', linestyle='dashed', linewidth=2, label=f'Mean: {mean_voltage_group:.3f} V')
plt.axvline(lower_voltage_cutoff, color='red', linestyle='dashed', linewidth=2, label=f'Lower Cutoff: {lower_voltage_cutoff:.3f} V')
plt.axvline(upper_voltage_cutoff, color='red', linestyle='dashed', linewidth=2, label=f'Upper Cutoff: {upper_voltage_cutoff:.3f} V')

plt.xlabel('Mean Voltage (V)')
plt.ylabel('Frequency')
plt.title('Histogram of Mean Voltages per Dataset with Bell Curve')
plt.legend()
plt.grid(True)
plt.show()

# Plot 3: Voltage vs. Discharge Capacity with Average Curve
plt.figure(figsize=(12, 6))

for dataset in filtered_datasets:
    plt.plot(dataset['Discharge Capacity (Ah)'], dataset['Voltage (V)'], alpha=0.1, color='gray')

plt.plot(average_capacity_curve['Discharge Capacity (Ah)'], average_capacity_curve['Voltage (V)'], 'r--', linewidth=2, label='Average Curve')

plt.ylim(2.5, 3.6)
plt.xlabel('Discharge Capacity (Ah)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs. Discharge Capacity with Average Curve')
plt.legend(loc='best')
plt.grid(True)
plt.show()
