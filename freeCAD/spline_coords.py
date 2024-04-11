import FreeCAD
import csv

#spline = FreeCAD.ActiveDocument.getObject('spline_tube')
doc = FreeCAD.getDocument('draft_tube')  # Get the document by name
obj = doc.getObject('Body')  # Get the object by name within the document
# Example: Accessing a sketch by its label
spline = doc.getObjectsByLabel('spline_tube')[0]  # Replace 'SketchLabel' with the actual label


# Discretize the spline
# The argument is the number of points you want to generate along the spline
discretized_points = spline.Shape.discretize(100)

# Now, discretized_points contains FreeCAD.Vector objects for each point along the spline

# Extract X, Z coordinates
points_xz = [(pt.x, pt.z) for pt in discretized_points]


# Path to the CSV file
csv_file_path = "D:/UCL/Research Assistant/ml-engineering/code/OPSIDIAN/freeCAD/spline_points.csv"

# Write to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Z"])  # Optional header
    writer.writerows(points_xz)
