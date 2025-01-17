# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 14:01:06 2024

@author: DanielDomikaitis
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Set the directory containing all folders with data
root_directory = r"C:\_git\inventory\testData"

# Define lists to store data for overlay plots and max discharge energy values
voltage_discharge_energy_data = []
voltage_charge_energy_data = []
max_discharge_energy_values = []

# Loop through each folder in the root directory
for folder_name in os.listdir(root_directory):
    folder_path = os.path.join(root_directory, folder_name)

    # Check if it's a directory
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")
        
        # Locate the required CSV files
        global_info_file = None
        wb_file = None
        
        # Print all files in the current folder for verification
        all_files = os.listdir(folder_path)
        print(f"  Files in folder: {all_files}")

        # Locate the desired files by matching the name pattern (look for '_Wb_' in the filename)
        for file_name in all_files:
            if "GlobalInfo" in file_name and file_name.endswith(".csv"):
                global_info_file = os.path.join(folder_path, file_name)
            elif "_Wb_" in file_name and file_name.endswith(".CSV"):
                wb_file = os.path.join(folder_path, file_name)

        # If no 'Wb' file was found, print a message and skip to the next folder
        if not wb_file:
            print(f"  No 'Wb' file found in folder: {folder_name}")
            continue

        # Read and process the 'Wb' CSV file for plotting
        print(f"  Reading file: {wb_file}")
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(wb_file)

            # Print out column names for debugging
            print(f"    Columns in file: {list(df.columns)}")

            # Ensure the required columns are present
            if all(col in df.columns for col in ['Voltage (V)', 'Charge Energy (Wh)', 'Discharge Energy (Wh)']):
                print(f"    Required columns found in file.")

                # Check if the maximum value of 'Discharge Energy (Wh)' is at least 300 Whr
                max_discharge_energy = df['Discharge Energy (Wh)'].max()
                print(f"    Max Discharge Energy in file: {max_discharge_energy} Whr")

                # Skip this file if the maximum discharge energy is less than 300 Whr
                if max_discharge_energy < 300:
                    print(f"    Skipping file due to insufficient maximum Discharge Energy (Whr) < 300.")
                    continue

                # Store the maximum discharge energy value for statistical analysis
                max_discharge_energy_values.append(max_discharge_energy)

                # Extract data for Voltage vs. Charge Energy
                charge_energy = df[['Voltage (V)', 'Charge Energy (Wh)']].dropna()
                voltage_charge_energy_data.append(charge_energy)

                # Extract data for Voltage vs. Discharge Energy
                discharge_energy = df[['Voltage (V)', 'Discharge Energy (Wh)']].dropna()
                voltage_discharge_energy_data.append(discharge_energy)
            else:
                # Print missing columns
                missing_cols = [col for col in ['Voltage (V)', 'Charge Energy (Wh)', 'Discharge Energy (Wh)'] if col not in df.columns]
                print(f"    Missing columns: {missing_cols}")
        except Exception as e:
            print(f"    Failed to process file {wb_file}: {e}")

# Plot Voltage vs. Discharge Energy overlay
if voltage_discharge_energy_data:
    plt.figure(figsize=(12, 6))
    for data in voltage_discharge_energy_data:
        if not data.empty:  # Check if there is any data left after filtering
            plt.plot(data['Discharge Energy (Wh)'], data['Voltage (V)'], alpha=0.6)
    plt.title("Overlay of Voltage vs. Discharge Energy (Filtered for Files with ≥300 Whr)")
    plt.xlabel("Discharge Energy (Wh)")
    plt.ylabel("Voltage (V)")
    plt.ylim(2, 3.8)  # Set the y-axis limit to show only 2-3.8 V
    plt.grid(True)
    plt.show()
else:
    print("No Voltage vs. Discharge Energy data to plot.")

# Plot Voltage vs. Charge Energy overlay
if voltage_charge_energy_data:
    plt.figure(figsize=(12, 6))
    for data in voltage_charge_energy_data:
        plt.plot(data['Charge Energy (Wh)'], data['Voltage (V)'], alpha=0.6)
    plt.title("Overlay of Voltage vs. Charge Energy")
    plt.xlabel("Charge Energy (Wh)")
    plt.ylabel("Voltage (V)")
    plt.ylim(2, 3.8)  # Set the y-axis limit to show only 2-3.8 V
    plt.grid(True)
    plt.show()
else:
    print("No Voltage vs. Charge Energy data to plot.")

# Plot the statistical analysis of maximum discharge energy values
if max_discharge_energy_values:
    plt.figure(figsize=(12, 6))

    # Plot histogram of the maximum discharge energy values
    count, bins, ignored = plt.hist(max_discharge_energy_values, bins=15, density=True, alpha=0.6, color='g', label="Histogram of Max Discharge Energy")

    # Fit a normal distribution to the data
    mu, sigma = np.mean(max_discharge_energy_values), np.std(max_discharge_energy_values)
    best_fit_line = stats.norm.pdf(bins, mu, sigma)
    plt.plot(bins, best_fit_line, '--', color='black', label=f'Gaussian Fit: μ={mu:.2f}, σ={sigma:.2f}')

    # Add a nominal value line at 336 Whr
    plt.axvline(x=336, color='blue', linestyle='-', linewidth=2, label='Nominal Value: 336 Whr')

    # Add mean and standard deviation lines
    plt.axvline(x=mu, color='red', linestyle='-', linewidth=2, label=f'Mean: {mu:.2f} Whr')
    plt.axvline(x=mu + sigma, color='orange', linestyle='--', linewidth=2, label=f'+1σ: {mu + sigma:.2f} Whr')
    plt.axvline(x=mu - sigma, color='orange', linestyle='--', linewidth=2, label=f'-1σ: {mu - sigma:.2f} Whr')
    plt.axvline(x=mu + 2 * sigma, color='purple', linestyle='--', linewidth=2, label=f'+2σ: {mu + 2 * sigma:.2f} Whr')
    plt.axvline(x=mu - 2 * sigma, color='purple', linestyle='--', linewidth=2, label=f'-2σ: {mu - 2 * sigma:.2f} Whr')
    plt.axvline(x=mu + 3 * sigma, color='brown', linestyle='--', linewidth=2, label=f'+3σ: {mu + 3 * sigma:.2f} Whr')
    plt.axvline(x=mu - 3 * sigma, color='brown', linestyle='--', linewidth=2, label=f'-3σ: {mu - 3 * sigma:.2f} Whr')

    # Add labels and legend
    plt.title("Statistical Distribution of Maximum Discharge Energy Values")
    plt.xlabel("Discharge Energy (Wh)")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No maximum discharge energy values to plot for statistical analysis.")
