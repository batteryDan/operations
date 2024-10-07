from rembg import remove
from PIL import Image

# Define the path to the input and output images
input_path = r'C:\_git\operations\headshots\angel.jpg'
output_path = r'C:\_git\operations\headshots\angel.jpg'

# Open the input image
with Image.open(input_path) as img:
    # Remove the background
    img_no_bg = remove(img)

    # Create a new image with a white background
    white_bg = Image.new('RGB', img_no_bg.size, (255, 255, 255))
    
    # Paste the image with the removed background onto the white background
    white_bg.paste(img_no_bg, mask=img_no_bg.split()[3])  # Use the alpha channel as the mask

    # Save the resulting image
    white_bg.save(output_path)

# Display the result
white_bg.show()
