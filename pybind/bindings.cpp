#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

namespace py = pybind11;

// Forward declaration of the modified main function
int poisson_recon_main(int argc, char* argv[]);

int run_poisson_recon(const std::vector<std::string>& args) {
    // Convert vector<string> to char* array for main()
    std::vector<char*> argv;
    argv.push_back(const_cast<char*>("PoissonRecon")); // argv[0] is program name
    for (const auto& arg : args) {
        argv.push_back(const_cast<char*>(arg.data()));
    }
    argv.push_back(nullptr);

    return poisson_recon_main(argv.size() - 1, argv.data());
}

PYBIND11_MODULE(poisson_recon_cpp, m) {
    m.doc() = "Python bindings for Screened Poisson Surface Reconstruction";
    m.def("run_poisson_recon", &run_poisson_recon, "Run the PoissonRecon executable logic with the given arguments");
}
