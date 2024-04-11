import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct

        # Get the selection
        selections = ui.activeSelections

        # Path to save the CSV file
        filepath = 'D:/UCL/Research Assistant/ml-engineering/code/OPSIDIAN/fusion360/point_extraction_plane_output.csv'

        # Open the file for writing
        with open(filepath, 'w') as file:
            file.write('Y,Z\n')  # Write the header row

            # Iterate over each selected entity
            for selection in selections:
                entity = selection.entity

                # Check if the entity is a sketch point
                if type(entity) is adsk.fusion.SketchPoint:
                    # Get the point geometry
                    point = entity.geometry

                    # Write the coordinates to the file
                    file.write(f'{point.x*10},{point.y*10}\n')

        # Inform the user that the export is complete
        ui.messageBox('Export complete!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

