import Part 
import FreeCAD as App
from CfdOF.Mesh import CfdMesh
from CfdOF import CfdTools
from CfdOF.Mesh import CfdMeshTools
from CfdOF import CfdConsoleProcess

def mesh(object:Part, mesh_size:float=50.8):
    """
    Function to mesh the object in freeCAD
    
    Parameters:
    object (Part.Shape): The object to be meshed
    mesh_size (float): The size of the mesh elements in mm
    """
    # create a cfd mesh object
    CfdMesh.makeCfdMesh('Sweep_Mesh')
    mesh = App.ActiveDocument.Sweep_Mesh
    mesh.Part = object
    CfdTools.getActiveAnalysis().addObject(mesh)
    mesh.CharacteristicLengthMax = str(mesh_size)
    cart_mesh = CfdMeshTools.CfdMeshTools(mesh)
    cart_mesh.writeMesh()

    # run the mesh
    proxy = mesh.Proxy
    proxy.cart_mesh = cart_mesh
    cart_mesh.error = False
    cmd = CfdTools.makeRunCommand('Allmesh.bat', source_env=False)
    env_vars = CfdTools.getRunEnvironment()
    proxy.running_from_macro = True
    if proxy.running_from_macro:
        mesh_process = CfdConsoleProcess.CfdConsoleProcess()
        mesh_process.start(cmd, env_vars=env_vars, working_dir=cart_mesh.meshCaseDir)
        mesh_process.waitForFinished()
    else:
        proxy.mesh_process.start(cmd, env_vars=env_vars, working_dir=cart_mesh.meshCaseDir)