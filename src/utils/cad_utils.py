
import FreeCAD

def clear_doc():
    """
    This function clears the documents so that FreeCAD does not need to be restarted to run updated code.
    """
    doc = FreeCAD.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Name)
    doc.recompute()