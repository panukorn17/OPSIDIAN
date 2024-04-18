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

if __name__ == "__main__":
    # Input plane
    plane = 2

    # Load polar coordinates data
    df_polar = pd.read_csv(f'src/data/baseline_draft_tube/plane_{plane}/polar_coordinates.csv')

    # Load spline details data
    df_spline = get_spline_details('src/data/baseline_draft_tube/spline')

    # Drop missing values
    df = df.dropna()

    # Save data
    df.to_csv("data/processed_data.csv", index=False)