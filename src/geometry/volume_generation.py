import gmsh
from pathlib import Path
from geometry.face_generation import calculate_face_coords, generate_faces_gmsh

def generate_solid(face_wires):
    return gmsh.model.occ.addThruSections(face_wires, makeSolid=True)

def get_groups(surface_tags):
    xs = []
    for s in surface_tags:
        # get the centre of the surfaces (denoted by 2)
        cx, cy, cz = gmsh.model.occ.getCenterOfMass(2,s)
        xs.append((cx, s))
    xs.sort(key=lambda t: t[0]) #sort by cx
    inlet = xs[0][1]
    outlet = xs[-1][1]
    walls = [s for _, s in xs[1:-1]]
    return inlet, outlet, walls

def generate_tube(baseline_factor: list[float]):
    gmsh.model.add("faces")
    faces_coordinate = calculate_face_coords(baseline_factor, Path('src')/ 'data')
    face_wires = generate_faces_gmsh(faces_coordinate)
    solid = generate_solid(face_wires)
    gmsh.model.occ.synchronize()
    # get the boundary surfaces of the volume denoted by 3 (volume)
    boundary = gmsh.model.getBoundary(solid)
    # get the surface tags (denoted by 2) of the boundary surfaces 
    surface_tags = [tag for (dim,tag) in boundary if dim==2]
    inlet_tag, outlet_tag, wall_tags = get_groups(surface_tags)
    # add name to the surfaces
    physical_group_inlet = gmsh.model.addPhysicalGroup(2, [inlet_tag])
    gmsh.model.setPhysicalName(2, physical_group_inlet, "inlet")
    
    physical_group_outlet = gmsh.model.addPhysicalGroup(2, [outlet_tag])
    gmsh.model.setPhysicalName(2, physical_group_outlet, "outlet")
    physical_group_wall = gmsh.model.addPhysicalGroup(2, wall_tags)
    gmsh.model.setPhysicalName(2, physical_group_wall, "tubeWall")
    gmsh.write("runs/gmsh/preview.brep")
    return

