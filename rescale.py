import os
from PIL import Image

# Paths for the input and output folders
input_folder = 'photos'
output_folder = 'lofi_photos'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to rescale the image to a target size (in KB) and max dimension of 1024 pixels
def rescale_image(input_path, output_path, target_size_kb, max_dimension):
    with Image.open(input_path) as img:
        # Resize image to ensure the largest dimension is max_dimension
        if max(img.size) > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
        
        quality = 95  # Start with high quality
        
        while True:
            # Save the image to the output path with the current quality
            img.save(output_path, 'JPEG', quality=quality)
            
            # Check the size of the saved image
            size_kb = os.path.getsize(output_path) / 1024
            
            # If the size is less than or equal to the target size, stop the loop
            if size_kb <= target_size_kb:
                break
            
            # Otherwise, decrease the quality
            quality -= 5
            if quality < 5:
                break  # Prevent quality from going to 0

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        rescale_image(input_path, output_path, 200, 1024)

print("Image rescaling completed.")
