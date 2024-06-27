import math

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