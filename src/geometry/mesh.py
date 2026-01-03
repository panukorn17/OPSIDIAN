import gmsh
def mesh(min_len:float=5.0, max_len:float=20.0):
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", min_len)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", max_len)

    gmsh.model.mesh.generate(3)
    gmsh.write("runs/gmsh/preview.msh")
    return