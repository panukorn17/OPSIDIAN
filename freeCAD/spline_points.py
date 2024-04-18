import FreeCAD
import csv
import Draft

# user input plane number to spline
plane_number = input("Enter the plane number")

# define file path
file_path = f"D:/UCL/Research Assistant/ml-engineering/code/OPSIDIAN/src/data/baseline_draft_tube/draft_tube_1/points_plane_{plane_number}_XYZ.csv"

# Read the CSV file and extract points from csv file as a tuple of x, y, z coordinates
with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    points = [(float(row[0]), float(row[1]), float(row[2])) for row in csv_reader]

# Convert the points to FreeCAD Vector objects, as required by the makeBSpline function
vectorPoints = [FreeCAD.Vector(pt[0], pt[1], pt[2]) for pt in points]


# Create the wire as a B-Spline curve
spline = Draft.makeBSpline(points, closed=True, face=True)
spline.ViewObject.LineColor = (0.0, 0.0, 1.0)  # Change the spline color to blue
spline.ViewObject.LineWidth = 2.0  # Change the spline line width
