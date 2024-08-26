import cv2
import numpy as np

def load_tif_image(image_path):
    # Load the .tif image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    return image

def crop_image_y_axis(image, num_crops=3):
    # Get the dimensions of the image
    height, width = image.shape[:2]
    
    # Calculate the height of each crop
    crop_height = height // num_crops
    
    # Create a list to hold the cropped images
    cropped_images = []
    
    for i in range(num_crops):
        y_start = i * crop_height
        y_end = (i + 1) * crop_height if i < num_crops - 1 else height
        crop = image[y_start:y_end, :]
        cropped_images.append(crop)
    
    return cropped_images

def save_cropped_images(cropped_images, base_filename):
    for idx, crop in enumerate(cropped_images):
        filename = f"{base_filename}_crop_{idx + 1}.tif"
        cv2.imwrite(filename, crop)

# Example usage
image_path = 'scans/R1/R1-May23-2-16bGrayScale-6400dpi-right.tif'
image = load_tif_image(image_path)
cropped_images = crop_image_y_axis(image, num_crops=3)
save_cropped_images(cropped_images, 'output_image')

