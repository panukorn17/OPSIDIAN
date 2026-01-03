################################################################################################################
################################### RUNNING SCRIPT ON FREECAD ##################################################
################################################################################################################
#----------------------------------------------------------------------------------------------------------------
# To run this script on FreeCAD, copy and paste the following commands to the FreeCAD Python console

# DIR = 'path to the directory containing the OPSIDIAN folder'
# exec(open(f'{DIR}/src/main.py').read())

# Update DIR with the path to the directory containing the OPSIDIAN folder
#----------------------------------------------------------------------------------------------------------------
################################################################################################################

from pathlib import Path
import gmsh
from utils.face_generation import calculate_face_coords, generate_faces_gmsh
# from utils.face_generation import , add_spine, sweep
# from utils.cfd_utils import create_analysis_container , setup_fluid_properties
# from utils.mesh_utils import mesh

DATA_DIR = Path('src')/ 'data'

if __name__ == "__main__":
    baseline_factor = [0.75, 0.25]
    base_element_size = 20 #mm
    gmsh.initialize()
    gmsh.model.add("faces")
    faces_coordinate = calculate_face_coords(baseline_factor, DATA_DIR)
    face_wires = generate_faces_gmsh(faces_coordinate)
    solid = gmsh.model.occ.addThruSections(face_wires, makeSolid=True)
    gmsh.model.occ.synchronize()
    print("out:", solid, "volumes:", gmsh.model.getEntities(3))
    gmsh.write("src/runs/gmsh/preview.brep")
    # optional: global mesh size
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 5.0)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 20.0)

    gmsh.model.mesh.generate(3)
    gmsh.write("src/runs/gmsh/preview.msh")
    gmsh.finalize()
    # spine = add_spine()
    # sweep = sweep(face_shapes, spine)
    # create_analysis_container()
    # setup_fluid_properties()
    # mesh(sweep, base_element_size)
