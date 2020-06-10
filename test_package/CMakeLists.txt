cmake_minimum_required(VERSION 3.13)
project(MathglTest CXX)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
find_package(mathgl MODULE REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example mathgl::mathgl)
