import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import math

DIR = "D:/UCL/Research Assistant/ml-engineering/code/OPSIDIAN/src/data/baseline_draft_tube"
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct

        # Ask the user for the number of the plane
        user_input = ui.inputBox('Enter the number of the plane to extract points from:', 'Plane Number', 'Enter Number')

        # Change the user input to an integer
        user_input = int(user_input[0])

        # Get the selection
        selections = ui.activeSelections

        # Path to save the CSV file
        filepath = f'{DIR}/draft_tube_{user_input}/points_plane_{user_input}_XYZ.csv'

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Open the file for writing
        with open(filepath, 'w') as file:
            file.write('type, local_X, local_Y, local_Z, phi_rad, phi_deg, radial_distance\n')  # Write the header row
            
            # initialise the polar angle
            delta_phi = 2*math.pi / len(selections)
            phi = -delta_phi

            # Iterate over each selected entity
            for i in range(len(selections)):
                # Assuming that the first entity is the centre point
                if i == 0:
                    center_point = selections.item(i).entity
                    if type(center_point) is adsk.fusion.SketchPoint:
                        center_point = center_point.geometry
                        file.write(f'center, {center_point.x*10},{center_point.y*10},{center_point.z*10}, 0, 0, 0\n')
                else:
                    # For the remaining edge points
                    edge_point = selections.item(i).entity

                    # Check if the entity is a sketch point
                    if type(edge_point) is adsk.fusion.SketchPoint:
                        # Get the point geometry
                        edge_point = edge_point.geometry

                        # Calculate the distance between the center and edge points
                        distance = center_point.distanceTo(edge_point)
                        
                        # Polar angle calculation in radians and degrees
                        phi += delta_phi
                        phi_deg = math.degrees(phi)

                        # Write the coordinates to the file
                        file.write(f'edge, {edge_point.x*10},{edge_point.y*10},{edge_point.z*10}, {phi}, {phi_deg}, {distance} \n')

        # Inform the user that the export is complete
        ui.messageBox('Export complete!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

