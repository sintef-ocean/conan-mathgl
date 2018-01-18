from conans import ConanFile, CMake, tools


class MathglConan(ConanFile):
    name = "mathgl"
    version = "2.4.1"
    license = "LGPL-3/GPL-3"
    url = "https://github.com/joakimono/conan-mathgl"
    author = "Joakim Haugen (joakim.haugen@gmail.com)"
    homepage ="http://mathgl.sourceforge.net"
    description = "MathGL is a library for making high-quality scientific graphics under Linux and Windows."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]} # expose more options: lgpl=1, openmp=0, pthr-widget=0, ..
    # position_independent_code:bool=on, mgl_have_c99_complex=0, cxx_flags=-std=c++11
    # 
    default_options = "shared=False"
    generators = "cmake"
    source_file ="mathgl-2.4.1.tar.gz"
    source_dir = "mathgl"
    requires = "zlib/[>=1.2.11]@conan/stable", "libpng/[>=1.6.34]@bincrafters/stable"
    # need to add more dependencies (configure or requirements function (depending on options)
    # opengl libharu, libjpeg, glut, qt5

    def source(self):
    
        link = "https://sourceforge.net/projects/mathgl/files/mathgl/mathgl%20{0}/mathgl-{0}.tar.gz".format(self.version)
        tools.get(link, sha1="6560acd7572fe4146c4adb62b3832c072ba74604")
        
        tools.replace_in_file("mathgl/CMakeLists.txt", "cmake_minimum_required(VERSION 2.8.12)",
        '''cmake_minimum_required(VERSION 3.1.2)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_dir)
        cmake.build()

    def package(self):
        self.copy("COPYING*", dst="licenses", src=self.source_dir,
                  ignore_case=True, keep_path=False) # TODO: copy LGPL or GPL depending on option

    def package_info(self):
        self.cpp_info.libs = ["mgl"]
        if not self.options.shared and self.settings.os == "Windows":
            self.cpp_info.libs[0] += "-static"
        if self.settings.build_type == "Debug" and self.settings.os == "Windows":
            self.cpp_info.libs[0] += "d"
        