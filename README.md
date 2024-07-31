# Optimising Design with Simulation-Based Bayesian Optimisation (OPSIDIAN)

## Introduction
The design process generally involves the following steps: modelling, analysis, and refinement. The initial modelling stage generally uses an overdesigned proposal. From here, it is up to the engineer to optimise the design by considering factors such as performance, cost, and construction time through iterative analysis and refinement procedures. The analysis step is crucial in this procedure and usually consists of Computational Fluid Dynamics (CFD) simulations or Finite Element Analysis (FEA) simulations. This calculates the performance metrics of a design and is the basis on which the design is optimised. Analysis is an expensive process. This presents opportunities to utilise machine learning to accelerate this process. Specifically, using surrogate models to predict simulation outcomes and Bayesian Optimisation to achieve optimal design efficiently. 
Key issues lie in the complexity of geometric representation and parameterisation. Examples include the curse of dimensionality with increasing variables describing a geometry or the fact that many parametric approaches can also lead to invalid design (Sikirica et al. 2024).
This research aims to create a novel framework for efficient design optimisation by integrating simulation-based analysis, surrogate models, and Bayesian Optimisation with te following workflow:  
<img src="images/OPSIDIAN_workflow.svg" height="700" alt="OPSIDIAN_workflow">  

## Prerequisites
To run this code please download FreeCAD and follow the instructions to setup OpenFOAM and ParaView.
1. FreeCAD: [Download Link](https://www.freecad.org/downloads.php)
2. Launch FreeCAD and download required addons:
    - Go to **Tools > Addon manager**   
    - Locate the **CfdOF** and **Plot Workbench** addons and install them.  
    <img src="images/2_2_install_addons.png" height="310" alt="2_1_tools_addon_manager">  
3. Download and setup OpenFOAM and ParaView:
    - Go to **Edit > Preferences**
    - Open the **CfdOF** ribon
    - Install OpenFoam (1)
    - Install ParaView (2)  
    - Locate and add OpenFoam directory (3) e.g. _"C:/Program Files/ESI-OpenCFD/OpenFOAM/v2212"_
    - Locate and add ParaView directory (4) e.g. _"C:/Program Files/ParaView 5.10.1-Windows-Python3.9-msvc2017-AMD64/bin/paraview.exe"_  
    <img src="images/3_OpenFOAM_ParaView.png" height="600" alt="3_OpenFOAM_ParaView">  

## Getting Started

To get started, follow these steps:

1. **Clone Repository**
2. Open FreeCAD and open python console through **View > Panels > Python console**
3. Run script by copying and pasting the following commands to the FreeCAD Python console (Update DIR with the path to the directory containing the OPSIDIAN folder):
```
DIR = 'path to the directory containing the OPSIDIAN folder'  
exec(open(f'{DIR}/src/main.py').read())  
```
## Some Engineering
As detailed by Sheikh et al. (2022), kinetic or potential energy not converted to mechanical energy of the turbine shaft is wasted. To minimise energy loss (maximise conversion of KE and PE to ME), the draft tube needs to be optimised to maximise the _dimensionless mean pressure recovery coefficient_:
$$C_{prm} \equiv \frac{P_2 - P_1}{\frac{1}{2} \rho v_1^2}$$
By maximising this coefficient, the theoretically available power, $\dot{W}$ is also maximised, where:
$$\dot{W} = A_0 v_0 (\Delta P)$$
$$\Delta P \equiv P_0 - P_1$$
and therefore we can make substitutions and the power becomes a function of the mean pressure recovery coefficient:
$$\dot{W} = A_0 v_0 \left(P_0 - P_2 + C_{prm}\left(\frac{\rho v_1^2}{2}\right)\right)$$
The parameters are as follows:
- $A_0$: cross-sectional area of the flow upstream of the turbine blade (**FIXED**)
- $v_0$: characteristic velocities upstream of the turbine (**FIXED**)
- $v_1$: characteristic velocities downstream of the turbine (**FIXED**)
- $P_0$: average fluid pressure upstream of the turbine (**FIXED**)
- $P_1$: average fluid pressure downstream of the turbine (**NUMERICAL SIMULATION**)
- $P_2$: average fluid pressure at the end of the draft tube (**FIXED**)
- $\rho$: density of the fluid (water)


# References
Sheikh, Haris Moazam, Tess A. Callan, Kealan J. Hennessy, and Philip S. Marcus. “Optimization of the Shape of a Hydrokinetic Turbine’s Draft Tube and Hub Assembly Using Design-by-Morphing with Bayesian Optimization.” Computer Methods in Applied Mechanics and Engineering 401 (November 2022): 115654. https://doi.org/10.1016/j.cma.2022.115654.
