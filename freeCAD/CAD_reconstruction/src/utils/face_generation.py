import FreeCAD as App
import Part
import csv
import math
from typing import List, Tuple

centres = [(0, 0, 0), #plane 1
            (5.333, 0, -144.623), #plane 2
            (36.791, 0, -289.331), #plane 3
            (91.665, 0, -426.512), #plane 4
            (167.629, 0, -554.016), #plane 5
            (279.67, 0, -656.591), #plane 6
            (407.779, 0, -737.83), #plane 7
            (536.748, 0, -799.26), #plane 8
            (672.528, 0, -835.133), #plane 9
            (814.82, 0, -847.56), #plane 10
            (977.817, 0, -845.565), #plane 11
            (1138.74, 0, -831.448), #plane 12
            (1300.874, 0, -802.406), #plane 13
            (1458.53, 0, -761.29), #plane 14
            (1780.247, 0, -673.92), #plane 15
            (2101.965, 0, -586.55), #plane 16
            (2423.682, 0, -499.18), #plane 17
            (2745.40, 0, -411.81), #plane 18
            (3235.68, 0, -274.137), #plane 19
            (3560.09, 0, -178.196), #plane 20
            (3876.111, 0, -76.161), #plane 21
            (4049.151, 0, -25.67), #plane 22
            (4137.633, 0, -4.381), #plane 23
            (4223.608, 0, 7.547), #plane 24
            (4281.578, 0, 12.828), #plane 25
            (4375.87, 0, 17.209)] #plane 26


def get_cartesian_coords(centre_coords, phi_rad, polar_radial_distance, theta):
    """
    This function converts the local polar coordinates to cartesian coordinates.

    Parameters:    
    centre_coords (tuple): Tuple containing the centre coordinates.
    polar_coords (list of dict): List containing the polar coordinates.
    theta (float): Angle of the spline at the plane in radians.

    Returns:
    cartesian_coords (list of tuple): List containing the cartesian coordinates.
    """
    cartesian_coords = []
    for i in range(len(phi_rad)):
        x_global = centre_coords[0] + polar_radial_distance[i] * math.cos(phi_rad[i]) * math.cos(theta) * 10
        y_global = centre_coords[1] + polar_radial_distance[i] * math.sin(phi_rad[i]) * 10
        z_global = centre_coords[2] + polar_radial_distance[i] * math.cos(phi_rad[i]) * math.sin(theta) * 10
        cartesian_coords.append((x_global, y_global, z_global))
    return cartesian_coords

def gradient_to_spline_angle(m):
    """
    Function to convert the gradient of the spline in the x-z plane to the angle of the spline starting from the north direction going anti-clockwise.

    Parameters:
    m (float): Gradient of the spline in the x-z plane.

    Returns:
    angle (float): Angle of the spline starting from the north direction going anti-clockwise.
    """
    if m == float('inf'):
        angle = 0
    elif m <= 0:
        angle = math.pi / 2 - math.atan(-m)
    else:
        angle = math.atan(m) + math.pi / 2
    return angle

def get_spline_details(dir):
    """
    This function gets the spline details and calculates the angle of the spline at the plane in radians and degrees if the columns are not already present.

    Parameters:
    dir (str): Directory of the spline details data.

    Returns:
    df_spline (list of dict): List containing the spline details. e.g. 
    [{'plane': '1', 'tangent_grad': '0.0', 'angle_rad': 0.0, 'angle_deg': 0.0}, ...]
    """
    spline_details = []
    with open(f'{dir}/spline_details.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            spline_details.append(row)

    for row in spline_details:
        if 'angle_rad' not in row:
            tangent_grad = float(row['tangent_grad'])
            angle_rad = gradient_to_spline_angle(tangent_grad)
            row['angle_rad'] = angle_rad
            row['angle_deg'] = math.degrees(angle_rad)

    return spline_details

def calculate_face_coords(baseline_factor: List)->List[Tuple]:
    """
    This function calculates the coordinates of the faces of the tube using the baseline factors
    to determine the shape of the face.
    
    Parameters:
    baseline_factor (list): List containing the baseline factors.

    Returns:
    faces_coordinates (list of tuple): List containing the coordinates of the faces of the tube.
    """
    print('Calculating face coordinates...')
    df_spline = get_spline_details('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/fusion360/reconstruction/data/spline')
    faces_coordinates = []
    for plane in range(1, 27):
            phi_rad = []
            polar_radial_distance = []
            for baseline in range(1,3):
                with open(f'C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/fusion360/reconstruction/data/baseline_{baseline}/plane_{plane}/polar_coordinates.csv', mode='r') as file:
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
    """

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

def add_spine():
    """
    This function adds the spine to the freeCAD document.

    Parameters:
    spine_coordinates (list of tuple): List containing the coordinates of the spine.
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

if __name__ == "__main__":
    baseline_factor = [1, 1]
    faces_coordinate = calculate_face_coords(baseline_factor)
    generate_faces(faces_coordinate)
    add_spine()
    #exec(open('C:/Users/ASUS/UCL/Research Assistant/code/OPSIDIAN/freeCAD/CAD_reconstruction/src/utils/face_generation.py').read())
