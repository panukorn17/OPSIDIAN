import gmsh
from geometry.volume_generation import generate_tube
from geometry.mesh import mesh

def main():
    baseline_factor = [0.2, 0.8]
    gmsh.initialize()
    generate_tube(baseline_factor)
    mesh()
    gmsh.finalize()
    return 

if __name__ == "__main__":
    main()
