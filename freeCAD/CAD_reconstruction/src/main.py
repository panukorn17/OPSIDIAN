# append the path to the sys.path
import sys
sys.path.append('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/freeCAD/CAD_reconstruction/src')

from utils.face_generation import calculate_face_coords, generate_faces, add_spine, sweep

if __name__ == "__main__":
    baseline_factor = [0.8, 0.3]
    faces_coordinate = calculate_face_coords(baseline_factor)
    face_shapes = generate_faces(faces_coordinate)
    spine = add_spine()
    sweep(face_shapes, spine)
    #exec(open('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/freeCAD/CAD_reconstruction/src/main.py').read())
