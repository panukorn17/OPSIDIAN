import Part 
import FreeCAD
from CfdOF import CfdAnalysis
from CfdOF import CfdTools
from CfdOF.Solve import CfdPhysicsSelection, CfdFluidMaterial, CfdInitialiseFlowField, CfdSolverFoam

def create_analysis_container():
    """
    Function to create the analysis container on freeCAD

    Parameters:
    shape (Part.Shape): The object to be analysed
    """
    # create a cfd analysis group object
    analysis = CfdAnalysis.makeCfdAnalysis('CfdAnalysis')
    CfdTools.setActiveAnalysis(analysis)
    analysis.addObject(CfdPhysicsSelection.makeCfdPhysicsSelection())
    analysis.addObject(CfdFluidMaterial.makeCfdFluidMaterial('FluidProperties'))
    analysis.addObject(CfdInitialiseFlowField.makeCfdInitialFlowField())
    analysis.addObject(CfdSolverFoam.makeCfdSolverFoam())