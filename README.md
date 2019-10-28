[![Download](https://api.bintray.com/packages/joakimono/conan/mathgl%3Ajoakimono/images/download.svg)](https://bintray.com/joakimono/conan/mathgl%3Ajoakimono/_latestVersion)
[![Build Status UNIX](https://travis-ci.org/joakimono/conan-mathgl.png?branch=master)](https://travis-ci.org/joakimono/conan-mathgl)
[![Build Status WIND](https://ci.appveyor.com/api/projects/status/github/joakimono/conan-mathgl?branch=master&svg=true)](https://ci.appveyor.com/project/joakimono/conan-mathgl)


[Conan.io](https://conan.io) recipe for [mathgl](http://mathgl.sourceforge.net).

The recipe generates library packages, which can be found at [Bintray](https://bintray.com/joakimono/conan/mathgl%3Ajoakimono).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add joakimono https://api.bintray.com/conan/joakimono/conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   mathgl/[>=2.4.4]@joakimono/stable

   [options]
   mathgl:shared=False

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.1.2)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup(TARGETS)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor CONAN_PKG::mathgl)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install ..
   ```
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

Option | Default | Domain
---|---|---
shared|True|[True, False]
lgpl|True|[True, False]
double_precision|True|[True, False]
rvalue_support|False|[True, False]
pthread|False|[True, False]
pthr_widget|False|[True, False]
openmp|True|[True, False]
opengl|True|[True, False]
glut|False|[True, False]
fltk|False|[True, False]
wxWidgets|False|[True, False]
qt5|False|[True, False]
zlib|True|[True, False]
png|True|[True, False]
jpeg|True|[True, False]
gif|False|[True, False]
pdf|True|[True, False]
gsl|False|[True, False]
hdf5|False|[True, False]
mpi|False|[True, False]
ltdl|False|[True, False]
all_swig|False|[True, False]

## Known recipe issues

* *fltk*, *wxWidgets*, *qt5*, *glut*, *hdf5*, *ltdl*, *opengl* will not currently be acquired with conan mechanisms, as such, the desired package(s) must be installed manually.
* There is a future plan to make a recipe for the *hdf5* dependency, there also exists a recipe in conan-transit, I believe.
* Not all options have been exposed into to the recipe option
* *rvalue* enabled does not currently compile
* Not tested for mingw or cygwin on Windows.
* Possible JPEG version mismatch (62 vs 80) on Windows (TBD)
