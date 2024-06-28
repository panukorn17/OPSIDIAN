import FreeCAD
import Mesh
import MeshPart
import csv

# Specify the output CSV file path
output_csv_path = "D:/UCL/Research Assistant/ml-engineering/code/OPSIDIAN/freeCAD/point_extraction_output.csv"

# Assuming the solid object is the first object in the document
solid = FreeCAD.ActiveDocument.Objects[0]

# Check if the object is already a mesh
if solid.TypeId.startswith("Mesh::Feature"):
    mesh = solid.Mesh
else:
    # Convert the solid to mesh if it's not a mesh
    mesh_quality = 0.1  # Adjust based on the desired mesh quality
    angular_deflection = 0.5  # Adjust based on the desired angular precision
    mesh = MeshPart.meshFromShape(Shape=solid.Shape, LinearDeflection=mesh_quality, AngularDeflection=angular_deflection, Relative=False)

# Now, `mesh` is the Mesh object you want to work with
# Exporting vertices to a CSV file
with open(output_csv_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['X', 'Y', 'Z'])  # Header for CSV file

    for vertex in mesh.Topology[0]:
        # Write the vertex coordinates to the CSV file
        csv_writer.writerow([vertex.x, vertex.y, vertex.z])

print(f"Mesh vertices exported to '{output_csv_path}'.")

