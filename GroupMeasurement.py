import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def normalize_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    if len(image.shape) == 3:  # Check if the image is RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    binary_image = binary_image // 255  # Normalize to 0 and 1
    return binary_image

def measure_regions(binary_image, x1, x2, y1, y2):
    white_lengths = []
    black_lengths = []
    second_black_lengths = []
    contoured_image = cv2.cvtColor(binary_image * 255, cv2.COLOR_GRAY2BGR)
    
    for y in range(y1, y2):
        row = binary_image[y, x1:x2]
        
        in_segment = False
        start_x = x1
        current_color = binary_image[y, x1]
        black_segment_count = 0
        
        for x in range(x1, x2):
            if binary_image[y, x] != current_color:
                length = x - start_x
                if current_color == 1:  # White segment
                    white_lengths.append(length)
                    cv2.line(contoured_image, (start_x, y), (x - 1, y), (255, 0, 0), 1)
                else:  # Black segment
                    black_lengths.append(length)
                    black_segment_count += 1
                    if black_segment_count == 2:
                        second_black_lengths.append(length)
                        cv2.line(contoured_image, (start_x, y), (x - 1, y), (0, 0, 255), 1)  # Blue color for second black area
                start_x = x
                current_color = binary_image[y, x]
        
        # Check the last segment
        length = x2 - start_x
        if current_color == 1:  # White segment
            white_lengths.append(length)
        else:  # Black segment
            black_lengths.append(length)
            black_segment_count += 1
            if black_segment_count == 2:
                second_black_lengths.append(length)
                cv2.line(contoured_image, (start_x, y), (x2 - 1, y), (0, 0, 255), 1)  # Blue color for second black area
    
    average_white_length = np.mean(white_lengths) if white_lengths else 0
    average_second_black_length = np.mean(second_black_lengths) if second_black_lengths else 0

    print(f"white_lengths: {white_lengths}")
    print(f"black_lengths: {black_lengths}")
    print(f"average_white_length: {average_white_length}")
    print(f"average_second_black_length: {average_second_black_length}")

    return white_lengths, black_lengths, average_white_length, average_second_black_length, contoured_image

def pixels_to_micrometers(dpi, pixels):
    micrometers_per_inch = 25400
    micrometers_per_pixel = micrometers_per_inch / dpi
    if isinstance(pixels, np.ndarray):
        return pixels * micrometers_per_pixel
    elif isinstance(pixels, (list, tuple)):
        return [pixel * micrometers_per_pixel for pixel in pixels]
    elif isinstance(pixels, (int, float)):
        return pixels * micrometers_per_pixel

def process_folder(folder_path, dpi, x1, y1, x2, y2, output_csv):
    # Create the output CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Image', 'Average_White_Length (µm)', 'Average_Second_Black_Length (µm)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each image in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                binary_image = normalize_image(image_path)

                # Ensure coordinates are within bounds
                img_height, img_width = binary_image.shape 
                x2_adjusted = min(x2, img_width)
                y2_adjusted = min(y2, img_height)
                x1_adjusted = max(0, min(x1, img_width-1))
                y1_adjusted = max(0, min(y1, img_height-1))

                print(f"Processing {filename} with region ({x1_adjusted}, {y1_adjusted}) to ({x2_adjusted}, {y2_adjusted})")

                # Measure the lengths of white regions and black gaps within the specified region
                _, _, average_white_length, average_second_black_length, _ = measure_regions(binary_image, x1_adjusted, x2_adjusted, y1_adjusted, y2_adjusted)
                
                # Convert pixel measurements to micrometers
                micrometers_L1 = pixels_to_micrometers(dpi, average_white_length)
                micrometers_L2 = pixels_to_micrometers(dpi, average_second_black_length)
                
                # Write results to CSV
                writer.writerow({
                    'Image': filename,
                    'Average_White_Length (µm)': micrometers_L1/0.269,
                    'Average_Second_Black_Length (µm)': micrometers_L2/0.269
                })
#/0.269
def main():
    # Parameters
    folder_path = 'R1D27-v100sxm2/images'  # Updated path to include the mounted directory
    dpi = 6400
    x1, y1 = 45, 110
    #x1, y1 = 45, 110
    x2, y2 = 230, 158
    #x2, y2 = 230, 158
    output_csv = 'R1D27_output.csv'  # Updated path to include the mounted directory

    # Process the folder
    process_folder(folder_path, dpi, x1, y1, x2, y2, output_csv)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    main()






















