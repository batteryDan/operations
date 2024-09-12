# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 18:24:22 2024

@author: DanielDomikaitis
"""

import os
from PIL import Image

# Define the folder path
folder_path = r'C:\_git\operations\headshots'

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a .tif or .cr2
    if filename.lower().endswith(('.tiff', '.tif', '.cr2')):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Open the image
        with Image.open(file_path) as img:
            # Convert to RGB if needed and save as .jpg
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_file_path = os.path.join(folder_path, jpg_filename)
            img.convert('RGB').save(jpg_file_path, 'JPEG')

        print(f"Converted {filename} to {jpg_filename}")
