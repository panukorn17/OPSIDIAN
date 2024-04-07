import Mesh
import MeshPart

# Assuming the imported 3MF file is a solid object and it's the first object
solid = App.ActiveDocument.Objects[0]

# Parameters for the mesh conversion
# These might need to be adjusted based on the desired quality and complexity of the mesh
mesh_quality = 1.0  # Lower values result in finer meshes
angular_deflection = 0.5  # Controls the angular precision of the mesh

# Create a mesh from the solid object
mesh = MeshPart.meshFromShape(Shape=solid.Shape, 
                              LinearDeflection=mesh_quality, 
                              AngularDeflection=angular_deflection, 
                              Relative=False)

# Add the mesh to the document
mesh_obj = App.ActiveDocument.addObject("Mesh::Feature", "MeshObject")
mesh_obj.Mesh = mesh
App.ActiveDocument.recompute()

print("Conversion to mesh completed.")
