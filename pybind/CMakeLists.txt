cmake_minimum_required(VERSION 3.14)
project(poisson_recon_bindings LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

# Find Python and Pybind11
find_package(Python 3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Include main project directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../Src)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/..)

# Create the module
pybind11_add_module(poisson_recon_cpp
    bindings.cpp
    # We need to compile the source file again because we cannot easily link against an executable object
    # without deeper surgery on the main CMakeLists.txt (creating an OBJECT library).
    ../Src/PoissonRecon.cpp
    # Add other necessary source files that PoissonRecon.cpp depends on, if any.
    # Based on the Makefile, it seems mostly header-only templates, but let's check.
)

# Important: Define the macro to exclude the main() function from PoissonRecon.cpp
target_compile_definitions(poisson_recon_cpp PRIVATE POISSON_RECON_NO_MAIN)

# Link dependencies
target_link_libraries(poisson_recon_cpp PRIVATE OpenMP::OpenMP_CXX Threads::Threads ZLIB::ZLIB PNG::PNG JPEG::JPEG)

# Install instruction for scikit-build-core
install(TARGETS poisson_recon_cpp LIBRARY DESTINATION poisson_recon)
