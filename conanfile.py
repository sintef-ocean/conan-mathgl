#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class MathglConan(ConanFile):
    name = "mathgl"
    version = "2.4.4"
    license = "LGPL-3.0 | GPL-3.0"
    licenses = ["LGPL-3.0", "GPL-3.0"]
    # LGPL-3.0-only | GPL-3.0-only
    url = "https://github.com/sintef-ocean/conan-mathgl"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    homepage = "http://mathgl.sourceforge.net"
    description = \
        "MathGL is a library for making high-quality scientific graphics "\
        "under Linux and Windows."
    topics = ("mathgl", "graphics", "plotting")
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")
    source_subfolder = "mathgl-{}".format(version)
    build_subfolder = "build_subfolder"
    exports_sources = "patch/*"
    options = {"shared": [True, False],
               "lgpl": [True, False],
               "double_precision": [True, False],
               "rvalue_support": [True, False],
               "pthread": [True, False],
               "pthr_widget": [True, False],
               "openmp": [True, False],
               "opengl": [True, False],
               "wxWidgets": [True, False],
               "qt5": [True, False],
               "zlib": [True, False],
               "png": [True, False],
               "jpeg": [True, False],
               "gif": [True, False],
               "pdf": [True, False],
               "gsl": [True, False],
               "hdf5": [True, False],
               "mpi": [True, False],
               "ltdl": [True, False],
               "all_swig": [True, False]
               }
    #          "glut": [True, False],
    #          "fltk": [True, False],
    default_options = ("shared=False",
                       "lgpl=True",
                       "double_precision=True",
                       "rvalue_support=False",
                       "pthread=True",
                       "pthr_widget=True",
                       "openmp=False",
                       "opengl=True",
                       "wxWidgets=False",
                       "qt5=False",
                       "zlib=True",
                       "png=True",
                       "jpeg=True",
                       "gif=True",
                       "pdf=True",
                       "gsl=False",
                       "hdf5=False",
                       "mpi=False",
                       "ltdl=False",
                       "all_swig=False")
    #                  "glut=False",
    #                  "fltk=False",
    cmake_options = {}

    def add_cmake_opt(self, val, doAdd):
        if doAdd:
            self.cmake_options["enable-{}".format(val)] = 'ON'
        else:
            self.cmake_options["enable-{}".format(val)] = 'OFF'

    def requirements(self):

        self.add_cmake_opt("lgpl", self.options.lgpl)
        self.add_cmake_opt("double", self.options.double_precision)
        self.add_cmake_opt("rvalue", self.options.rvalue_support)
        self.add_cmake_opt("pthread", self.options.pthread)
        self.add_cmake_opt("pthr-widget", self.options.pthr_widget)
        self.add_cmake_opt("openmp", self.options.openmp)
        self.add_cmake_opt("opengl", self.options.opengl)
        # self.add_cmake_opt("glut", self.options.glut)
        # self.add_cmake_opt("fltk", self.options.fltk)
        self.add_cmake_opt("wxWidgets", self.options.wxWidgets)
        self.add_cmake_opt("qt5", self.options.qt5)
        self.add_cmake_opt("zlib", self.options.zlib)
        self.add_cmake_opt("png", self.options.png)
        self.add_cmake_opt("jpeg", self.options.jpeg)
        self.add_cmake_opt("gif", self.options.gif)
        self.add_cmake_opt("pdf", self.options.pdf)
        self.add_cmake_opt("mpi", self.options.mpi)
        self.add_cmake_opt("ltdl", self.options.ltdl)
        if not self.options.lgpl:
            self.add_cmake_opt("gsl", self.options.gsl)
            self.add_cmake_opt("hdf5", self.options.hdf5)
            self.add_cmake_opt("all-swig", self.options.all_swig)

        # TODO add dependencies using conan packages
        # expected to be found w/o conan: glut, fltk, ltdl, gsl, mpi

        if self.settings.os != "Windows" and self.options.opengl:
            self.requires("opengl/virtual@bincrafters/stable")

        if self.options.zlib:
            self.requires("zlib/[>=1.2.11]@conan/stable")
        if self.options.png:
            self.requires("libpng/[>=1.6.34]@bincrafters/stable")
        if self.options.jpeg:
            self.requires("libjpeg-turbo/[>=1.5.2 <2.0]@bincrafters/stable")
            # set jpeg version 62
        if self.options.gif:
            self.requires("giflib/[>=5.1.4]@bincrafters/stable")
        if self.options.pdf:
            self.requires("libharu/[>=2.3.0]@sintef/stable")
        if self.options.hdf5:
            if not self.options.lgpl:
                self.requires("hdf5/[>=1.8.21]@sintef/stable")

        if self.options.wxWidgets:
            self.requires("wxwidgets/[>=3.1.0]@bincrafters/stable")
        if self.options.qt5:
            self.requires("qt/[>=5.10.0]@bincrafters/stable")

    def source(self):

        link = "https://sourceforge.net/projects/mathgl/files/mathgl/mathgl%20{0}/mathgl-{0}.tar.gz".format(self.version)
        tools.get(link, sha1="c7faa770a78a8b6783a4eab6959703172f28b329") # sha1 is for 2.4.4

        tools.patch(patch_file="patch/CMakeLists.patch", base_path=self.source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions.update(self.cmake_options)
        if self.options.shared and self.settings.os == "Windows":
            cmake.definitions["enable-dep-dll"] = "ON"
        cmake.configure(source_folder=self.source_subfolder,
                        build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def build_id(self):
        self.info_build.options.shared = "Any"

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("*.pdb", dst="lib")

        if self.options.lgpl:
            theLicense = 'COPYING_LGPL'
        else:
            theLicense = 'COPYING'
        self.copy(theLicense, dst="licenses", src=self.source_subfolder,
                  ignore_case=True, keep_path=False)
        if self.options.shared:
            pass  # The dynamic version is needed for the bin/mglconv

    def package_info(self):
        self.cpp_info.name = 'MathGL'
        self.cpp_info.builddirs.append("cmake")
        self.cpp_info.libs = ["mgl"]
        if self.options.qt5:
            self.cpp_info.libs.append('mgl-qt5')
            self.cpp_info.libs.append('mgl-qt')
        if self.options.wxWidgets:
            self.cpp_info.libs.append('mgl-wx')

        if not self.options.shared and self.settings.compiler == "Visual Studio":
            for lib in range(len(self.cpp_info.libs)):
                self.cpp_info.libs[lib] += "-static"
            self.cpp_info.libs.append("mgl")
