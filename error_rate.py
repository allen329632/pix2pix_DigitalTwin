import pandas as pd
import numpy as np
import re

# Load the fake measurements CSV file
fake_measurements_path = 'MeasureF/bz16_real_B.csv'

# Read the CSV file into a DataFrame
fake_data = pd.read_csv(fake_measurements_path)

# Function to extract width and gap from the image name
def extract_width_gap(image_name):
    match = re.search(r'w(\d+)_g(\d+)', image_name)
    if match:
        width = int(match.group(1))
        gap = int(match.group(2))
        return width, gap
    return None, None

# Apply the function to extract width and gap
fake_data[['Width', 'Gap']] = fake_data['Image'].apply(lambda x: pd.Series(extract_width_gap(x)))

# Filter out rows where width or gap extraction failed
fake_data = fake_data.dropna(subset=['Width', 'Gap'])

# Rename columns to match the new terminology
fake_data.rename(columns={
    'Average_White_Length (µm)': 'Measured_Width',
    'Average_Second_Black_Length (µm)': 'Measured_Gap'
}, inplace=True)

# Define the optimal additions
optimal_width_addition = 50
optimal_gap_addition = 100

# Calculate the optimal values (width and gap) with the optimal additions
fake_data['Optimal_Width'] = fake_data['Width'] + optimal_width_addition
fake_data['Optimal_Gap'] = fake_data['Gap'] + optimal_gap_addition

# Calculate error rates based on the optimal values
def calculate_error(optimal, measured):
    return np.round(np.abs(optimal - measured) / optimal * 100, 3)  # Convert to percentage and round to three decimal places

fake_data['Width_Error (%)'] = calculate_error(
    fake_data['Optimal_Width'],
    fake_data['Measured_Width']
)

fake_data['Gap_Error (%)'] = calculate_error(
    fake_data['Optimal_Gap'],
    fake_data['Measured_Gap']
)

# Display the results
error_rates = fake_data[['Image', 'Width_Error (%)', 'Gap_Error (%)']]


# Save the results to a new CSV file
output_path = 'bz16_realimage_error_rates.csv'
fake_data.to_csv(output_path, index=False)
print(f"Error rates saved to {output_path}")











