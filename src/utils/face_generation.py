import FreeCAD as App
import Part
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

def generate_faces(faces_coordinate: List[Tuple]):
    """
    This function generates faces in free cad using the calculated face coordinates.

    Parameters:
    faces_coordinate (list of tuple): List containing the coordinates of the faces of the tube.

    Returns:
    face_shapes (list of shapes): List containing the shapes of the faces.
    """
    face_shapes = []
    for face_coords in faces_coordinate:
        # create freeCAD points
        vec_points = [App.Vector(p[0], p[1], p[2]) for p in face_coords[1:]]
        vec_points.append(vec_points[0])

        # create spline from points
        spline = Part.BSplineCurve()
        spline.interpolate(vec_points)

        # Add spline to the app
        obj = App.ActiveDocument.addObject('Part::Feature', 'Spline')
        obj.Shape = spline.toShape()

        # recompute the document
        App.ActiveDocument.recompute()
        face_shapes.append(obj)
    return face_shapes

def add_spine():
    """
    This function adds the spine to the freeCAD document.

    Parameters:
    spine_coordinates (list of tuple): List containing the coordinates of the spine.

    Returns:
    Spine (shape): Shape of the spine.
    """
    # create freeCAD points
    spine_points = [App.Vector(coord[0], coord[1], coord[2]) for coord in centres]

    # create spline from points
    spine = Part.BSplineCurve()
    spine.interpolate(spine_points)

    # Add spline to the app
    obj = App.ActiveDocument.addObject('Part::Feature', 'Spine')
    obj.Shape = spine.toShape()

    # recompute the document
    App.ActiveDocument.recompute()

    return obj

def sweep(face_shapes: List, spine: Part.Shape)->Part.Shape:
    """
    This function performs a sweep operation in freeCAD.
    
    Parameters:
    face_shapes (list of shapes): List containing the shapes of the faces.
    spine (shape): Shape of the spine.

    Returns:
    sweep (shape): Shape of the sweep.
    """
    # create sweep object
    sweep = App.ActiveDocument.addObject('Part::Sweep', 'Sweep')
    sweep.Sections = face_shapes
    sweep.Spine = (spine,['Edge1',])
    sweep.Solid = True
    sweep.Frenet = False

    # recompute the document
    App.ActiveDocument.recompute()

    return sweep