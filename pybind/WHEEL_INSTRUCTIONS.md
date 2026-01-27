# Building the PoissonRecon Python Wheel

This guide explains how to package the PoissonRecon Python wrapper into a `.whl` file (Wheel) for distribution.

## Prerequisites

You need the following Python packages installed in your environment:

```bash
pip install build scikit-build-core pybind11 tyro
```

## Build Instructions

To generate the wheel, you **must** be inside the `pybind/` directory where the `pyproject.toml` file is located.

### 1. Navigate to the Pybind directory

```bash
cd pybind
```

### 2. Run the Build Command

Use the following command to build the wheel. We recommend menggunakan `--no-isolation` to use the dependencies already in your environment.

```bash
python -m build --wheel --no-isolation
```

## Output

Once the build finishes successfully, your wheel file will be located in the `pybind/dist/` folder:

```text
pybind/dist/poisson_recon-0.1.0-cp312-cp312-linux_x86_64.whl
```

## How to Share the Wheel

The generated wheel is a **Binary Distribution**. Because it contains a compiled `.so` extension:

- It will work on other **Linux x86_64** systems with the same **Python version**.
- **Important**: This wheel depends on system libraries (like `libpng`, `libjpeg`, and `libgomp`). For broad distribution, these should be bundled using a tool like `auditwheel`.

## Installation from Wheel

To install the generated wheel into a new environment:

```bash
pip install dist/poisson_recon-0.1.0-cp312-cp312-linux_x86_64.whl
```
