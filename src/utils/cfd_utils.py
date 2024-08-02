import Part 
import FreeCAD
import FreeCAD as App

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

def setup_physics_model(model, time='Steady', turbulence='Laminar', turbulenceModel='kOmegaSST'):
    """
    Function to set up the physics model for CfdOF
    """
    model.Time = time
    model.Turbulence = turbulence 
    model.TurbulenceModel = turbulenceModel

def setup_fluid_properties(name='Water', type='Isothermal', density='998 kg/m^3', dynamicViscosity='1.003e-3 kg/m/s'):
    """
    Function to set up the fluid properties for CfdOF
    """
    print("Setting up fluid proberties")
    if name == 'Water':
        desc = 'Standard distilled water properties at 20 Degrees Celsius and 1 atm'
        App.ActiveDocument.FluidProperties.Label = 'Water'
    else:
        desc = ''
        App.ActiveDocument.FluidProperties.Label = 'Fluid'
    App.ActiveDocument.FluidProperties.Material = {'CardName': name + type,
                                       'AuthorAndLicence': '',
                                       'Name': name,
                                       'Type': type,
                                       'Description': desc,
                                       'Density': density,
                                       'DynamicViscosity': dynamicViscosity}