import tyro
from dataclasses import dataclass
from typing import Optional
import sys
import os

# Import the C++ binding
# We assume the .so is in the same directory or PYTHONPATH
try:
    from . import poisson_recon_cpp
except ImportError:
    # Fallback for development if the .so is in build/python
    try:
        import poisson_recon_cpp
    except ImportError:
        print("Could not import poisson_recon_cpp binding. Please build the project first.")
        sys.exit(1)

@dataclass
class PoissonReconConfig:
    """
    Configuration for Screened Poisson Surface Reconstruction.
    """
    in_file: str
    """Input point set file (ply, bnpts, etc.)"""
    
    out_file: Optional[str] = None
    """Output triangle mesh file (ply)"""
    
    depth: int = 8
    """Maximum reconstruction depth (default: 8)"""
    
    full_depth: int = 5
    """Full depth (default: 5)"""
    
    cg_accuracy: float = 1e-3
    """CG Solver accuracy (default: 1e-3)"""
    
    point_weight: float = 4.0
    """Interpolation weight (default: 4.0)"""
    
    samples_per_node: float = 1.5
    """Minimum number of samples per node (default: 1.5)"""
    
    confidence: bool = False
    """Use confidence values from normals (default: False)"""
    
    linear_fit: bool = False
    """Use linear fitting (default: False)"""
    
    threads: int = 1
    """Number of OpenMP threads to use"""

    scale: float = 1.1
    """Scale factor (default: 1.1)"""
    
    width: float = 0.0
    """Grid width (default: 0.0 -> computed)"""
    
    iters: int = 8
    """Iterations (default: 8)"""
    
    base_depth: int = -1
    """Coarse MG solver depth (default: -1)"""
    
    base_v_cycles: int = 1
    """Coarse MG solver v-cycles (default: 1)"""
    
    envelope: Optional[str] = None
    """Input envelope file"""
    
    degree: int = 1
    """B-Spline degree (default: 1)"""
    
    b_type: int = 2
    """Boundary type (1: Free, 2: Dirichlet, 3: Neumann) (default: 2)"""
    
    # Boolean flags
    density: bool = False
    """Output estimated density values"""
    
    gradients: bool = False
    """Output gradients"""
    
    show_residual: bool = False
    """Show residual"""
    
    polygon_mesh: bool = False
    """Output polygon mesh instead of triangle mesh"""
    
    non_manifold: bool = False
    """Allow non-manifold output"""
    
    ascii: bool = False
    """Output in ASCII format"""
    
    verbose: bool = False
    """Verbose output"""

    def to_argv(self) -> list[str]:
        args = []
        args.extend(["--in", self.in_file])
        if self.out_file:
            args.extend(["--out", self.out_file])
        
        # Numbers
        args.extend(["--depth", str(self.depth)])
        args.extend(["--fullDepth", str(self.full_depth)])
        args.extend(["--cgAccuracy", str(self.cg_accuracy)])
        args.extend(["--pointWeight", str(self.point_weight)])
        args.extend(["--samplesPerNode", str(self.samples_per_node)])
        args.extend(["--scale", str(self.scale)])
        args.extend(["--iters", str(self.iters)])
        args.extend(["--baseVCycles", str(self.base_v_cycles)])
        args.extend(["--degree", str(self.degree)])
        args.extend(["--bType", str(self.b_type)])
        
        # Optional Numbers
        if self.width > 0:
            args.extend(["--width", str(self.width)])
        if self.base_depth >= 0:
            args.extend(["--baseDepth", str(self.base_depth)])

        # Optional Strings
        if self.envelope:
            args.extend(["--envelope", self.envelope])
        
        # Boolean Flags
        if self.confidence: args.append("--confidence")
        if self.linear_fit: args.append("--linearFit")
        if self.density: args.append("--density")
        if self.gradients: args.append("--gradients")
        if self.show_residual: args.append("--showResidual")
        if self.polygon_mesh: args.append("--polygonMesh")
        if self.non_manifold: args.append("--nonManifold")
        if self.ascii: args.append("--ascii")
        if self.verbose: args.append("--verbose")
            
        return args

    def main(self):
        """
        Run Poisson Reconstruction with the given configuration.
        """
        # Set OpenMP threads environment variable before calling C++
        os.environ["OMP_NUM_THREADS"] = str(self.threads)
        
        argv = self.to_argv()
        print(f"Running PoissonRecon with args: {argv}")
        
        # Call the C++ binding
        poisson_recon_cpp.run_poisson_recon(argv)

def entry_point():
    config = tyro.cli(tyro.conf.FlagConversionOff[PoissonReconConfig])
    config.main()

if __name__ == "__main__":
    entry_point()
