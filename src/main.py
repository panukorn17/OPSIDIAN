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

import sys
# append the path to the sys.path
sys.path.append(DIR + '/src')

import FreeCAD
import os

from pathlib import Path
from utils.face_generation import calculate_face_coords, generate_faces, add_spine, sweep
from utils.cfd_utils import create_analysis_container , setup_fluid_properties
from utils.cad_utils import clear_doc
from utils.mesh_utils import mesh

SRC_DIR = Path(DIR + '/src')
DATA_DIR = SRC_DIR / 'data'

if __name__ == "__main__":
    clear_doc()
    baseline_factor = [0.75, 0.25]
    base_element_size = 20 #mm
    faces_coordinate = calculate_face_coords(baseline_factor, DATA_DIR)
    face_shapes = generate_faces(faces_coordinate)
    spine = add_spine()
    sweep = sweep(face_shapes, spine)
    create_analysis_container()
    setup_fluid_properties()
    mesh(sweep, base_element_size)
