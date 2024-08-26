import gdspy
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Load the GDS file
gdsii = gdspy.GdsLibrary(infile='R1Layout.gds')

# Create a figure with black background
fig, ax = plt.subplots(figsize=(20, 20), dpi=500, facecolor='black')  # Increase figure size and DPI
ax.set_aspect('equal')
ax.set_facecolor('black')  # Set the axis background to black

# Draw all cells using the get_polygons method
for cell in gdsii.top_level():
    polygons = cell.get_polygons(by_spec=True)
    for (layer, datatype), polys in polygons.items():
        for poly in polys:
            polygon = Polygon(poly, closed=True, edgecolor='white', facecolor='white')
            ax.add_patch(polygon)

# Set limits and labels with white color
ax.autoscale_view()
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')

# Save the figure to a TIFF file with higher resolution
output_tiff_path = 'R1Layout.tiff'
fig.savefig(output_tiff_path, format='tiff', dpi=500)  # Save with higher DPI

# Show the path to the saved file
print(f"TIFF file saved to {output_tiff_path}")












