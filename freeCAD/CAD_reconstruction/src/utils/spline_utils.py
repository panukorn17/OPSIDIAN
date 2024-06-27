import math
import csv

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
    df_spline (list of dict): List containing the spline details.
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