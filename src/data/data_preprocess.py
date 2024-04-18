import pandas as pd
import numpy as np

def gradient_to_spline_angle(m:float)->float:
    """
    Function to convert the gradient of the spline in the x-z plane to the angle of the spline strarting from the north direction going anti-clockwise.

    Parameters:
    m (float): Gradient of the spline in the x-z plane.

    Returns:
    angle (float): Angle of the spline starting from the north direction going anti-clockwise.
    """
    if m == np.inf:
        # 0
        angle = 0
    elif m <= 0:
        # -arccot(m)
        angle = np.pi/2 - np.arctan(-m)
    elif m > 0:
        # arccot(m) + pi/2
        angle = np.arctan(m) + np.pi/2
    return angle

def get_spline_details(dir:str)->pd.DataFrame:
    """
    This function gets the spline details and calculates the angle of the spline at the plane in radians and degrees if the columns are not already present.

    Parameters:
    dir (str): Directory of the spline details data.

    Returns:
    df_spline (pd.DataFrame): Dataframe containing the spline details.
    """

    # Load spline details data
    df_spline = pd.read_csv(f'{dir}/spline_details.csv')

    # Check if the columns are already present
    if 'angle_rad' not in df_spline.columns:
        # calculate the angle of the spline at the plane in radians and degrees
        df_spline['angle_rad'] = df_spline['tangent_grad'].apply(gradient_to_spline_angle)
        df_spline['angle_deg'] = np.degrees(df_spline['angle_rad'])

        # save the data
        df_spline.to_csv(f'{dir}/spline_details.csv', index=False)

    return df_spline

def get_cartesian_coords(polar_coords:pd.DataFrame, theta:float)->pd.DataFrame:
    """
    This function converts the local polar coordinates to cartesian coordinates.

    Parameters:
    polar_coords (pd.DataFrame): Dataframe containing the polar coordinates.
    theta (float): Angle of the spline at the plane in radians.

    Returns:
    df_cartesian (pd.DataFrame): Dataframe containing the cartesian coordinates.
    """
    # Calculate the cartesian coordinates
    df_cartesian = pd.DataFrame()
    df_cartesian['X_global'] = polar_coords['radial_distance'] * np.cos(polar_coords['phi_rad']) * np.cos(theta)
    df_cartesian['Y_global'] = polar_coords['radial_distance'] * np.sin(polar_coords['phi_rad'])
    df_cartesian['Z_global'] = polar_coords['radial_distance'] * np.cos(polar_coords['phi_rad']) * np.sin(theta)

    # Save the data
    df_cartesian.to_csv(f'src/data/baseline_draft_tube/plane_{plane}/cartesian_coordinates.csv', index=False)

    return df_cartesian


if __name__ == "__main__":
    # Input plane
    plane = 2

    # Load polar coordinates data
    df_polar = pd.read_csv(f'src/data/baseline_draft_tube/plane_{plane}/polar_coordinates.csv')

    # Load spline details data
    df_spline = get_spline_details('src/data/baseline_draft_tube/spline')

    # Calculate the global cartesian coordinates of the plane
    theta = df_spline[df_spline['plane'] == plane]['angle_rad'].values[0]
    df_cartesian = get_cartesian_coords(df_polar, theta)