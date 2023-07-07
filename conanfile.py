import os
import re
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy, rmdir, rm
from conan.tools.files import apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.microsoft.visual import is_msvc
from conan.tools.scm import Version

required_conan_version = ">=1.53.0"


class MathglConan(ConanFile):
    name = "mathgl"
    license = "LGPL-3.0-only", "GPL-3.0-only"
    url = "https://github.com/sintef-ocean/conan-mathgl"
    author = "SINTEF Ocean"
    homepage = "http://mathgl.sourceforge.net"
    description = \
        "MathGL is a library for making high-quality scientific graphics "\
        "under Linux and Windows."
    topics = ("mathgl", "graphics", "plotting")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "lgpl": [True, False],
        "double_precision": [True, False],
        "rvalue_support": [True, False],
        "pthread": [True, False],
        "pthr_widget": [True, False],
        "all_swig": [True, False],
        "fltk": [True, False],
        "gif": [True, False],
        "gsl": [True, False],
        "hdf5": [True, False],
        "jpeg": [True, False],
        "ltdl": [True, False],
        "mpi": [True, False],
        "opengl": [True, False],
        "openmp": [True, False],
        "pdf": [True, False],
        "png": [True, False],
        "qt5": [True, False],
        "zlib": [True, False],
        "wxWidgets": [True, False],
        "glut": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "lgpl": True,
        "double_precision": True,
        "rvalue_support": False,
        "pthread": False,
        "pthr_widget": False,
        "all_swig": False,
        "fltk": False,
        "gif": False,
        "gsl": False,
        "hdf5": False,
        "jpeg": True,
        "ltdl": False,
        "mpi": False,
        "opengl": True,
        "openmp": False,
        "pdf": True,
        "png": True,
        "qt5": False,
        "zlib": True,
        "wxWidgets": False,
        "glut": False,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        if self.options.pdf:
            self.options["libharu*"].shared = False

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        # TODO add dependencies using conan packages
        # expected to be found w/o conan: glut, ltdl, mpi, wxwidgets

        if self.settings.os != "Windows" and self.options.opengl:
            self.requires("opengl/system")

        if self.options.zlib:
            self.requires("zlib/[~1.2.13]")
        if self.options.png:
            self.requires("libpng/1.6.39")
        if self.options.jpeg:
            self.requires("libjpeg/9e")
        if self.options.gif:
            self.requires("giflib/[~5.1.4]")
        if self.options.gsl:
            self.requires("gsl/2.7")
        if self.options.fltk:
            self.requires("fltk/1.3.8")
        if self.options.pdf:
            self.requires("libharu/[~2.3.0]")
        if self.options.hdf5:
            if not self.options.lgpl:
                self.requires("hdf5/[~1.8.21]")
        if self.options.qt5:
            self.requires("qt/[^5.15.9]")

    def validate(self):
        if self.options.qt5 and self.settings.compiler == "gcc" \
           and Version(self.settings.compiler.version) <= "6":
            raise ConanInvalidConfiguration(
                "With option qt5 enabled you need gcc >= 7")
        if is_msvc(self):
            if self.options.pthr_widget or self.options.pthread:
                raise ConanInvalidConfiguration(
                    "pthr_widget, pthread are incompatible with Visual Studio")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        on_off = lambda v: "ON" if v else "OFF"
        tc = CMakeToolchain(self)
        tc.variables["enable-lgpl"] = on_off(self.options.lgpl)
        tc.variables["enable-double"] = on_off(self.options.double_precision)
        tc.variables["enable-rvalue"] = on_off(self.options.rvalue_support)
        tc.variables["enable-pthread"] = on_off(self.options.pthread)
        tc.variables["enable-pthr-widget"] = on_off(self.options.pthr_widget)
        tc.variables["enable-openmp"] = on_off(self.options.openmp)
        tc.variables["enable-opengl"] = on_off(self.options.opengl)
        tc.variables["enable-glut"] = on_off(self.options.glut)
        tc.variables["enable-fltk"] = on_off(self.options.fltk)
        tc.variables["enable-wxWidgets"] = on_off(self.options.wxWidgets)
        tc.variables["enable-qt5"] = on_off(self.options.qt5)
        tc.variables["enable-zlib"] = on_off(self.options.zlib)
        tc.variables["enable-png"] = on_off(self.options.png)
        tc.variables["enable-jpeg"] = on_off(self.options.jpeg)
        tc.variables["enable-gif"] = on_off(self.options.gif)
        tc.variables["enable-pdf"] = on_off(self.options.pdf)
        tc.variables["enable-mpi"] = on_off(self.options.mpi)
        tc.variables["enable-ltdl"] = on_off(self.options.ltdl)
        if not self.options.lgpl:
            tc.variables["enable-gsl"] = on_off(self.options.gsl)
            tc.variables["enable-hdf5"] = on_off(self.options.hdf5)
            tc.variables["enable-all-swig"] = on_off(self.options.all_swig)

        tc.variables["enable-dep-dll"] = on_off(self.options.shared and
                                                self.settings.os == "Windows")
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

        # Add VirtualBuildEnv?

        for dep in self.dependencies.values():
            if dep.package_folder and os.path.exists(
                    os.path.join(dep.package_folder, "licenses")):
                copy(self, "*",
                     os.path.join(dep.package_folder, "licenses"),
                     os.path.join(self.build_folder, "licenses", dep.ref.name),
                     keep_path=True)

    def build(self):
        #env_build = RunEnvironment(self)
        #with tools.environment_append(env_build.vars):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        #env_build = RunEnvironment(self)
        #with tools.environment_append(env_build.vars):
        cmake = CMake(self)
        cmake.install()
        restatic = re.compile("(.*[.]a$)|(.*-static[.]lib)")
        redll = re.compile(".*[.]dll$")
        # Use conan tools instead?
        for root, dirs, files in os.walk(os.path.join(self.package_folder, "lib")):
            for file in files:
                if (self.options.shared and restatic.match(file)) or \
                   (not self.options.shared and not restatic.match(file)):
                    rm(self, file, root)
        if not self.options.shared and self.settings.os == "Windows":
            for root, dirs, files in os.walk(os.path.join(self.package_folder, "bin")):
                for file in files:
                    if redll.match(file):
                        rm(self, file, root)
        if self.settings.os == "Windows":
            rmdir(self, os.path.join(self.package_folder, "cmake"))
            rm(self, "mathgl2-config.cmake", self.package_folder)
        else:
            rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
            copy(self, "COPYING",
                 dst=os.path.join(self.package_folder, "licenses"),
                 src=self.source_folder,
                 ignore_case=True, keep_path=False)
        if self.options.lgpl:
            copy(self, "COPYING_LGPL",
                 dst=os.path.join(self.package_folder, "licenses"),
                 src=self.source_folder,
                 ignore_case=True, keep_path=False)
        copy(self, "*",
             dst=os.path.join(self.package_folder, "licenses"),
             src=os.path.join(self.build_folder, "licenses"), keep_path=True)

    def package_info(self):
        if is_msvc(self):
            self.cpp_info.builddirs.append("cmake")  # what/why is this?
        self.cpp_info.libs = ["mgl"]
        if self.options.qt5:
            self.cpp_info.libs.append("mgl-qt")
            self.cpp_info.libs.append("mgl-qt5")
        if self.options.wxWidgets:
            self.cpp_info.libs.append("mgl-wx")

        # TODO: should reflect actual targets and components as defined in package
        self.cpp_info.set_property("cmake_file_name", "MathGL")
        self.cpp_info.set_property("cmake_target_name", "MathGL::MathGL")

        if not self.options.shared:
            if is_msvc(self):
                for lib in range(len(self.cpp_info.libs)):
                    self.cpp_info.libs[lib] += "-static"
            self.cpp_info.defines = ["MGL_STATIC_DEFINE",
                                     "_CRT_STDIO_ISO_WIDE_SPECIFIERS"]
