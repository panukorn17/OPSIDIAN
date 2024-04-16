import FreeCAD

# Assuming the object of interest is the first object in the document
obj = FreeCAD.ActiveDocument.Objects[0]

# Accessing the first face of the object
face = obj.Shape.Faces[0]

center = face.CenterOfMass
print("Center coordinates:", center)