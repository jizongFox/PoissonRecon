cmake_minimum_required(VERSION 3.14)
project(PoissonRecon LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Dependencies
find_package(OpenMP REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(ZLIB REQUIRED)
find_package(PNG REQUIRED)
find_package(JPEG REQUIRED)

# Threads support (for -pthread)
find_package(Threads REQUIRED)

# Common compiler flags
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wno-deprecated -Wno-invalid-offsetof)
    # Architecture specific optimizations
    add_compile_options(-funroll-loops -ffast-math)
endif()

# Source directory inclusion
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Src)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Output directory (mimic Makefile behavior)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/build/bin)

# Helper function to add executable targets
function(add_poisson_executable name source_file)
    add_executable(${name} Src/${source_file})
    target_link_libraries(${name} PRIVATE OpenMP::OpenMP_CXX Threads::Threads)
    # Most targets need image libraries, so we link them by default.
    # We can refine this if needed.
    target_link_libraries(${name} PRIVATE ZLIB::ZLIB PNG::PNG JPEG::JPEG)
endfunction()

# --- TARGETS ---

# 1. PoissonRecon
add_poisson_executable(PoissonRecon PoissonRecon.cpp)

# 2. PoissonReconClient (Needs Boost)
add_executable(PoissonReconClient Src/PoissonReconClient.cpp)
target_link_libraries(PoissonReconClient PRIVATE OpenMP::OpenMP_CXX Threads::Threads Boost::system)

# 3. PoissonReconServer (Needs Boost)
add_executable(PoissonReconServer Src/PoissonReconServer.cpp)
target_link_libraries(PoissonReconServer PRIVATE OpenMP::OpenMP_CXX Threads::Threads Boost::system)

# 4. SSDRecon
add_poisson_executable(SSDRecon SSDRecon.cpp)

# 5. PointInterpolant
add_poisson_executable(PointInterpolant PointInterpolant.cpp)

# 6. SurfaceTrimmer
add_executable(SurfaceTrimmer Src/SurfaceTrimmer.cpp)
target_link_libraries(SurfaceTrimmer PRIVATE OpenMP::OpenMP_CXX Threads::Threads)

# 7. EDTInHeat
add_executable(EDTInHeat Src/EDTInHeat.cpp)
target_link_libraries(EDTInHeat PRIVATE OpenMP::OpenMP_CXX Threads::Threads)

# 8. ImageStitching
add_poisson_executable(ImageStitching ImageStitching.cpp)

# 9. AdaptiveTreeVisualization
add_poisson_executable(AdaptiveTreeVisualization AdaptiveTreeVisualization.cpp)

# 10. ChunkPLY
add_poisson_executable(ChunkPLY ChunkPLY.cpp)

# 11. ReconExample
add_poisson_executable(ReconExample Reconstruction.example.cpp)

# 12. PointsToDisks
add_executable(PointsToDisks Src/PointsToDisks.cpp)
target_link_libraries(PointsToDisks PRIVATE OpenMP::OpenMP_CXX Threads::Threads)

# 13. ScaleNormals
add_executable(ScaleNormals Src/ScaleNormals.cpp)
target_link_libraries(ScaleNormals PRIVATE OpenMP::OpenMP_CXX Threads::Threads)

# --- CONFIGURATION INFO ---
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER}")

# Python Bindings
add_subdirectory(pybind)
