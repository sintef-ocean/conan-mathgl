[![Linux GCC](https://github.com/sintef-ocean/conan-mathgl/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-mathgl/actions?query=workflow%3A"Linux+GCC")
[![Windows MSVC](https://github.com/sintef-ocean/conan-mathgl/workflows/Windows%20MSVC/badge.svg)](https://github.com/sintef-ocean/conan-mathgl/actions?query=workflow%3A"Windows+MSVC")

[Conan.io](https://conan.io) recipe for [mathgl](http://mathgl.sourceforge.net).

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:
   ```
   [requires]
   mathgl/2.4.4@sintef/stable

   [tool_requires]
   cmake/[>=3.25.0]

   [options]

   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv
   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.15)
   project(TheProject CXX)

   find_package(MathGL REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor MathGL::MathGL)
   ```
   Install and build e.g. a Release configuration:
   ```bash
   $ conan install . -s build_type=Release -pr:b=default
   $ source build/Release/generators/conanbuild.sh
   $ cmake --preset conan-release
   $ cmake --build build/Release
   $ source build/Release/generators/deactivate_conanbuild.sh
   ```

## Package options

Option | Default | Allowed values
---|---|---
shared   | False | [True, False]
fPIC     | True  | [True, False]
lgpl     | True  | [True, False]
double_precision | True  | [True, False]
rvalue_support | False  | [True, False]
pthread  | False  | [True, False]
pthr_widget | False  | [True, False]
all_swig | False | [True, False]
gif      | False  | [True, False]
glut     | False  | [True, False]
gsl      | False  | [True, False]
hdf5     | False  | [True, False]
jpeg     | True  | [True, False]
ltdl     | False  | [True, False]
mpi      | False  | [True, False]
opengl   | True  | [True, False]
openmp   | False | [True, False]
pdf      | True  | [True, False]
png      | True  | [True, False]
qt5      | False  | [True, False]
wxWidgets | False  | [True, False]
zlib     | True  | [True, False]

## Known recipe issues

- There are several options which may not work as they are not been tested, including: fltk, wxWidgets
- With Qt5 does not currently work
