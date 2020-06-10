[![GCC Conan](https://github.com/sintef-ocean/conan-mathgl/workflows/GCC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-mathgl/actions?query=workflow%3A"GCC+Conan")
[![Clang Conan](https://github.com/sintef-ocean/conan-mathgl/workflows/Clang%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-mathgl/actions?query=workflow%3A"Clang+Conan")
[![MSVC Conan](https://github.com/sintef-ocean/conan-mathgl/workflows/MSVC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-mathgl/actions?query=workflow%3A"MSVC+Conan")
[![Download](https://api.bintray.com/packages/sintef-ocean/conan/mathgl%3Asintef/images/download.svg)](https://bintray.com/sintef-ocean/conan/mathgl%3Asintef/_latestVersion)


[Conan.io](https://conan.io) recipe for [mathgl](http://mathgl.sourceforge.net).

The recipe generates library packages, which can be found at [Bintray](https://bintray.com/sintef-ocean/conan/mathgl%3Asintef).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add sintef https://api.bintray.com/conan/sintef-ocean/conan
   $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   mathgl/[>=2.6.2]@sintef/stable

   [options]
   mathgl:shared=False

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake_paths
   cmake_find_package
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(mathgl MODULE REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor mathgl::mathgl)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

Option | Default | Domain
---|---|---
shared   | True  | [True, False]
lgpl     | True  | [True, False]
double_precision | True  | [True, False]
rvalue_support | False  | [True, False]
pthread  | False  | [True, False]
pthr_widget | False  | [True, False]
openmp   | True  | [True, False]
opengl   | True  | [True, False]
glut     | False  | [True, False]
fltk     | False  | [True, False]
wxWidgets | False  | [True, False]
qt5      | False  | [True, False]
zlib     | True  | [True, False]
png      | True  | [True, False]
jpeg     | True  | [True, False]
gif      | False  | [True, False]
pdf      | True  | [True, False]
gsl      | False  | [True, False]
hdf5     | False  | [True, False], not yet supported
mpi      | False  | [True, False]
ltdl     | False  | [True, False]
all_swig | False | [True, False]

## Known recipe issues

Some
