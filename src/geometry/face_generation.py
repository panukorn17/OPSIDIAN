import gmsh
import csv

from pathlib import Path
from utils.face_utils import get_cartesian_coords
from utils.spline_utils import get_spline_details
from data.spline_coords import centres
from typing import List, Tuple

def calculate_face_coords(baseline_factor:List, data_dir:Path)->List[Tuple]:
    """
    This function calculates the coordinates of the faces of the tube using the baseline factors
    to determine the shape of the face.
    
    Parameters:
    baseline_factor (list): List containing the baseline factors.
    data_dir (str): Directory containing the data.

    Returns:
    faces_coordinates (list of tuple): List containing the coordinates of the faces of the tube.
    """
    print('Calculating face coordinates...')
    df_spline = get_spline_details(data_dir / 'spline')
    faces_coordinates = []
    for plane in range(1, 27):
            phi_rad = []
            polar_radial_distance = []
            for baseline in range(1,3):
                path = data_dir / f'baseline_{baseline}/plane_{plane}/polar_coordinates.csv'
                with open(path, mode='r') as file:
                    reader = csv.DictReader(file)
                    i = 0
                    for row in reader:
                        if baseline == 1:
                            polar_radial_distance.append(baseline_factor[baseline-1]*float(row['radial_distance']))
                            phi_rad.append(float(row['phi_rad']))
                        else:
                            polar_radial_distance[i] = (polar_radial_distance[i] + baseline_factor[baseline-1]*float(row['radial_distance']))
                            i += 1
            theta = float(next(row['angle_rad'] for row in df_spline if int(row['plane']) == plane))
            cartesian_coords = get_cartesian_coords(centres[plane-1], phi_rad, polar_radial_distance, theta)
            faces_coordinates.append(cartesian_coords)
    return faces_coordinates

def generate_faces_gmsh(faces_coordinate: List[Tuple]):
    """
    This function generates faces in free cad using the calculated face coordinates.

    Parameters:
    faces_coordinate (list of tuple): List containing the coordinates of the faces of the tube.

    Returns:
    face_shapes (list of shapes): List containing the shapes of the faces.
    """
    face_wires = []
    for face_coords in faces_coordinate:
        # adding points and storing the tags in a list
        pt_tags = [gmsh.model.occ.addPoint(x, y, z) for x,y,z in face_coords[1:]]
        pt_tags.append(pt_tags[0])

        # create spline from points of the face
        spline_tag = gmsh.model.occ.addSpline(pt_tags)
        wire_tag = gmsh.model.occ.addWire([spline_tag])
        face_wires.append(wire_tag)

    return face_wires

