# append the path to the sys.path
import sys
sys.path.append('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/freeCAD/CAD_reconstruction/src')

from utils.face_generation import calculate_face_coords, generate_faces, add_spine, sweep
from utils.cfd_utils import create_analysis_container
from utils.mesh_utils import mesh

if __name__ == "__main__":
    baseline_factor = [1, 1]
    base_element_size = 50.8 #mm
    faces_coordinate = calculate_face_coords(baseline_factor)
    face_shapes = generate_faces(faces_coordinate)
    spine = add_spine()
    sweep = sweep(face_shapes, spine)
    create_analysis_container()
    mesh(sweep, base_element_size)
    #exec(open('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/freeCAD/CAD_reconstruction/src/main.py').read())
