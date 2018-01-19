from conans import ConanFile, CMake, tools
import svn.remote

class MathglConan(ConanFile):
    name = "mathgl"
    version = "2.4.2"
    license = "LGPL-3.0-only | GPL-3.0-only"
    url = "https://github.com/joakimono/conan-mathgl"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    homepage ="http://mathgl.sourceforge.net"
    description = "MathGL is a library for making high-quality scientific graphics under Linux and Windows."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    source_dir = "mathgl-{}".format(version)
    exports_sources = "patch/*"
    options = {"shared": [True, False],
               "lgpl": [True, False],
               "double_precision": [True, False],
               "rvalue_support": [True, False],
               "pthread": [True, False],
               "pthr_widget": [True, False],
               "openmp": [True, False],
               "opengl": [True, False],
               "glut": [True, False],
               "fltk": [True, False],
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
    default_options = ("shared=True",
                       "lgpl=False",
                       "double_precision=True",
                       "rvalue_support=True",            
                       "pthread=False",
                       "pthr_widget=False",
                       "openmp=True",
                       "opengl=True",
                       "glut=False",
                       "fltk=False",
                       "wxWidgets=False",
                       "qt5=False",
                       "zlib=True",
                       "png=True",
                       "jpeg=True",
                       "gif=False",
                       "pdf=False",
                       "gsl=False",
                       "hdf5=False",
                       "mpi=False",
                       "ltdl=False",
                       "all_swig=False")
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
        self.add_cmake_opt("glut", self.options.glut)
        self.add_cmake_opt("fltk", self.options.fltk)
        self.add_cmake_opt("wx", self.options.wxWidgets)
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

        # expected to be found w/o conan: opengl, glut, fltk, mpi, ltdl, gsl
        if self.options.wxWidgets:
            self.requires("wxWidgets/[>3.0.3]@cjwddtc/stable") # shared linking?"
        if self.options.qt5:
            self.requires("qt5/[>=5.10]@joakimono/stable") #  shared linking?
        if self.options.zlib:
            self.requires("zlib/[>=1.2.11]@conan/stable", private=True)
            self.options["zlib"].shared = False
        if self.options.png:
            self.requires("libpng/[>=1.6.34]@bincrafters/stable", private=True)
            self.options["libpng"].shared = False
        if self.options.jpeg:
            self.requires("libjpeg-turbo/[>=1.5.2]@bincrafters/stable", private=True)
            self.options["libjpeg-turbo"].shared = False
# Currently does not link properly.
#        if self.options.gif:
#            self.requires("giflib/[>=5.1.3]@bincrafters/stable", private=True)
#            self.options["giflib"].shared = False
        if self.options.pdf:
            self.requires("libharu/[>=2.3.0]@joakimono/testing", private=True)
            self.options["libharu"].shared = False
        if self.options.hdf5:
            if not self.options.lgpl:
                self.requires("hdf5/[>=1.10.1]@joakimono/stable")
        
    def source(self):
    
        #The newest release has bugs (won't compile on windows): 2.4.1. Revert to this way once a functional release appears
        #link = "https://sourceforge.net/projects/mathgl/files/mathgl/mathgl%20{0}/mathgl-{0}.tar.gz".format(self.version)
        #tools.get(link, sha1="6560acd7572fe4146c4adb62b3832c072ba74604") # sha1 is for 2.4.1

        r = svn.remote.RemoteClient('https://svn.code.sf.net/p/mathgl/code/mathgl-2x')
        r.export('mathgl-{}'.format(self.version),revision=1544) # this revision is version 2.4.2
        
        tools.patch(patch_file="patch/CMakeLists.patch", base_path=self.source_dir)
        tools.patch(patch_file="patch/abstract.patch", base_path=self.source_dir)
        
    def build(self):
        cmake = CMake(self)
        cmake.definitions.update(self.cmake_options)
        cmake.configure(source_folder=self.source_dir)
        cmake.build()
        cmake.install()

        #        "shared=True", Both are built anyway: only 1 build 2 configs..
    def package(self):
        if self.options.lgpl:
            theLicense = 'COPYING_LGPL'
        else:
            theLicense = 'COPYING'
        self.copy(theLicense, dst="licenses", src=self.source_dir,
                  ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mgl"]
        if not self.options.shared and self.settings.os == "Windows":
            self.cpp_info.libs[0] += "-static"
        if self.settings.build_type == "Debug" and self.settings.os == "Windows":
            self.cpp_info.libs[0] += "d"
        
