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

        # Get the selection
        selections = ui.activeSelections

        # Path to save the CSV file
        filepath = f'{DIR}/spline/spline_details.csv'

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Open the file for writing
        with open(filepath, 'w') as file:
            # Write the header row
            file.write('plane, start_x_local, end_x_local, start_y_local, end_y_local, normal_grad, tangent_grad\n') 

            # Initialise plane number
            plane = 1

            # Iterate over each selected entity
            for selection in selections:
                # Get the selected entity
                entity = selection.entity

                # Calculate the gradient of the entity
                if type(entity) is adsk.fusion.SketchLine:
                    # Get the geometry of the line
                    line = entity

                    # Calculate the gradient of the line

                    # Get start and end points
                    start = line.startSketchPoint.geometry
                    end = line.endSketchPoint.geometry

                    # transform the points to the local coordinate system
                    start_x = end.x
                    end_x = start.x
                    start_y = -end.y
                    end_y = -start.y

                    # Caculate the gradient dz/dx
                    normal_grad = (end_y - start_y) / (end_x - start_x)

                    # Check if the gradient is zero
                    if normal_grad == 0:
                        tangent_grad = math.inf
                    else:
                        tangent_grad = -1 / normal_grad

                    # Write the details to the CSV file
                    file.write(f'{plane}, {start_x*10}, {end_x*10}, {start_y*10}, {end_y*10}, {normal_grad}, {tangent_grad}\n')

                    # Increment the plane number
                    plane += 1
                    
        # Inform the user that the export is complete
        ui.messageBox("Spline details exported!")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                