cmake_minimum_required(VERSION 3.13)
project(MathglTest CXX)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
find_package(MathGL MODULE REQUIRED)

option(WITH_QT "MathGL with qt5 enabled" OFF)
option(WITH_OPENGL "MathGL is opengl enabled" ON)

if(WITH_OPENGL)
  set(OpenGL_GL_PREFERENCE_LEGACY)
  find_package(OPENGL REQUIRED)
  message(STATUS "OPENGL_FOUND=${OPENGL_FOUND}")
  message(STATIS "OPENGL_LIBRARIES=${OPENGL_LIBRARIES}")
endif()

if(WITH_QT)
  find_package(Qt5 COMPONENTS Widgets REQUIRED)

  add_executable(qt_example qt_example.cpp)
  target_link_libraries(qt_example MathGL::MathGL Qt5::Widgets)
  set(WITH_QT_TARGET "Qt5::Widgets")
endif()

add_executable(example example.cpp)
target_link_libraries(example MathGL::MathGL ${WITH_QT_TARGET} ${OPENGL_LIBRARIES})
