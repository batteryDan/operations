import os
import math
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw
import face_recognition

# Define the folder path
folder_path = r'C:\_git\operations\headshots'

# Target size for the final image (e.g., 256x256 pixels)
target_size = (256, 256)

# Function to calculate the eye-to-eye distance
def calculate_eye_distance(face_landmarks):
    left_eye = face_landmarks['left_eye']
    right_eye = face_landmarks['right_eye']

    # Calculate the centers of the eyes
    left_eye_center = (
        sum([pt[0] for pt in left_eye]) / len(left_eye),
        sum([pt[1] for pt in left_eye]) / len(left_eye)
    )
    right_eye_center = (
        sum([pt[0] for pt in right_eye]) / len(right_eye),
        sum([pt[1] for pt in right_eye]) / len(right_eye)
    )

    # Calculate the distance between the eyes
    eye_distance = math.sqrt(
        (right_eye_center[0] - left_eye_center[0]) ** 2 +
        (right_eye_center[1] - left_eye_center[1]) ** 2
    )
    return eye_distance, left_eye_center, right_eye_center

# First pass: Calculate the average eye-to-eye distance across all images
def calculate_average_eye_distance():
    total_distance = 0
    count = 0

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg') and not filename.startswith("circular_"):
            file_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(file_path)
            face_landmarks_list = face_recognition.face_landmarks(image)

            if face_landmarks_list:
                eye_distance, _, _ = calculate_eye_distance(face_landmarks_list[0])
                total_distance += eye_distance
                count += 1

    average_distance = total_distance / count if count > 0 else 0
    return average_distance

# Function to subtly enhance image quality
def enhance_image_quality(image):
    # Enhance brightness, contrast, and color
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.05)  # Slightly increase brightness

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.1)  # Slightly increase contrast

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.1)  # Slightly increase color saturation

    return image

# Second pass: Process each image using the average eye-to-eye distance
def process_images(average_eye_distance, eye_shift=0.1, zoom_out_factor=1.3):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg') and not filename.startswith("circular_"):
            file_path = os.path.join(folder_path, filename)
            output_filename = f"circular_{filename}"
            output_path = os.path.join(folder_path, output_filename)

            # Check if the output file already exists
            if not os.path.exists(output_path):
                crop_face_to_circle(file_path, output_path, average_eye_distance, eye_shift, zoom_out_factor)
            else:
                print(f"Skipping {filename} as it already has a circular version.")

# Function to crop the face, level the eyes, and make it circular with transparency
def crop_face_to_circle(image_path, output_path, average_eye_distance, eye_shift=0.1, zoom_out_factor=1.3):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    
    # Find face and landmark locations
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_locations = face_recognition.face_locations(image)

    if face_locations and face_landmarks_list:
        # Take the first face detected
        top, right, bottom, left = face_locations[0]
        face_landmarks = face_landmarks_list[0]

        # Calculate eye distance and centers
        current_eye_distance, left_eye_center, right_eye_center = calculate_eye_distance(face_landmarks)

        # Calculate the zoom factor needed to achieve the average eye-to-eye distance
        zoom_factor = average_eye_distance / current_eye_distance

        # Calculate the angle between the eyes
        delta_x = right_eye_center[0] - left_eye_center[0]
        delta_y = right_eye_center[1] - left_eye_center[1]
        angle = math.degrees(math.atan2(delta_y, delta_x))

        # Open image with Pillow
        pil_image = Image.fromarray(image)

        # Rotate the image to level the eyes
        rotated_image = pil_image.rotate(angle, resample=Image.BICUBIC, center=(right_eye_center[0], right_eye_center[1]))

        # Resize the image based on zoom factor
        new_size = (int(pil_image.width * zoom_factor), int(pil_image.height * zoom_factor))
        resized_image = rotated_image.resize(new_size, Image.LANCZOS)

        # Calculate the new eye centers after resizing
        new_left_eye_center = (left_eye_center[0] * zoom_factor, left_eye_center[1] * zoom_factor)
        new_right_eye_center = (right_eye_center[0] * zoom_factor, right_eye_center[1] * zoom_factor)

        # Calculate the center of the face based on the eyes
        face_center_x = (new_left_eye_center[0] + new_right_eye_center[0]) / 2
        face_center_y = (new_left_eye_center[1] + new_right_eye_center[1]) / 2 + average_eye_distance * eye_shift

        # Calculate the radius for cropping with zoom out adjustment
        radius = int(average_eye_distance * 2 * zoom_out_factor)  # Adjusted radius for zoom out

        # Calculate the bounding box for the circular crop
        box = (int(face_center_x - radius), int(face_center_y - radius), int(face_center_x + radius), int(face_center_y + radius))

        # Crop the image to the bounding box
        cropped_image = resized_image.crop(box)

        # Create a circular mask with the same size as the cropped image
        mask = Image.new('L', cropped_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, cropped_image.size[0], cropped_image.size[1]), fill=255)

        # Apply the circular mask to the image
        circular_image = cropped_image.copy()
        circular_image.putalpha(mask)

        # Resize to the target size using LANCZOS filter
        final_image = circular_image.resize(target_size, Image.LANCZOS)

        # Enhance the image quality
        enhanced_image = enhance_image_quality(final_image)

        # Save the result with transparency
        enhanced_image.save(output_path, format='PNG')
        print(f"Saved circular headshot to {output_path}")

# Calculate the average eye-to-eye distance
average_eye_distance = calculate_average_eye_distance()

# Process all images using the calculated average eye-to-eye distance
process_images(average_eye_distance, eye_shift=0.1, zoom_out_factor=1.3)
