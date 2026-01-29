# Python Bindings for PoissonRecon

Python bindings for the Screened Poisson Surface Reconstruction algorithm.

## Installation

### Quick

```bash
pip install "git+https://github.com/jizongFox/PoissonRecon.git#subdirectory=pybind"
```


### Prerequisites

```bash
pip install pybind11 tyro scikit-build-core build
```

### Building the Wheel (Recommended for sharing)

See the detailed [WHEEL_INSTRUCTIONS.md](WHEEL_INSTRUCTIONS.md) guide.

### Build Locally (Development)

```bash
cd /path/to/PoissonRecon
mkdir build && cd build
cmake .. -Dpybind11_DIR=$(python -m pybind11 --cmakedir)
cmake --build . -j $(nproc)
```

The Python extension will be built at `build/pybind/poisson_recon_cpp.*.so`.

## Usage

### Command Line Interface

```bash
cd pybind
PYTHONPATH=../build/pybind:. python -m poisson_recon.cli \
    --in-file input.ply \
    --out-file output.ply \
    --depth 10
```

### View All Options

```bash
PYTHONPATH=../build/pybind:. python -m poisson_recon.cli --help
```

### Python API

```python
import sys
sys.path.insert(0, '../build/pybind')
import poisson_recon_cpp

# Run reconstruction
args = [
    '--in', 'input.ply',
    '--out', 'output.ply',
    '--depth', '10',
    '--verbose'
]
poisson_recon_cpp.run_poisson_recon(args)
```

## Parameters

| Parameter          | Type  | Default  | Description                  |
| ------------------ | ----- | -------- | ---------------------------- |
| `in_file`          | str   | required | Input point set file         |
| `out_file`         | str   | None     | Output mesh file             |
| `depth`            | int   | 8        | Maximum reconstruction depth |
| `full_depth`       | int   | 5        | Full depth                   |
| `point_weight`     | float | 4.0      | Interpolation weight         |
| `samples_per_node` | float | 1.5      | Min samples per node         |
| `confidence`       | bool  | False    | Use confidence values        |
| `linear_fit`       | bool  | False    | Use linear fitting           |
| `density`          | bool  | False    | Output density values        |
| `verbose`          | bool  | False    | Verbose output               |

See `--help` for the complete list of 20+ parameters.

## Architecture

- **C++ Bindings**: `pybind/bindings.cpp` uses pybind11 to expose the reconstruction function
- **CLI**: `pybind/poisson_recon/cli.py` uses tyro to generate a beautiful CLI from dataclasses
- **Build**: CMake integration compiles the extension alongside the main executables

## Notes

- The bindings use in-memory execution (no subprocess overhead)
- Global parameters are reset between runs to avoid state leakage
- Thread count can be controlled via `--config.threads`
