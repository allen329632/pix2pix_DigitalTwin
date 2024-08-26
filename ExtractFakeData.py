import pandas as pd
import os

# Path to the input CSV file
input_csv_path = 'MeasureF/bz16output.csv'

# Load the CSV data into a DataFrame
df = pd.read_csv(input_csv_path)

# Filter the DataFrame to include only rows where the Image contains 'fake_B'
filtered_df = df[df['Image'].str.contains('fake_B')]

# Define the directory path to save the filtered CSV file
directory_path = 'MeasureF'

# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

# Save the filtered DataFrame to a new CSV file in the directory
file_path = os.path.join(directory_path, 'bz16_fake_B.csv')
filtered_df.to_csv(file_path, index=False)

file_path


