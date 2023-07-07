cmake_minimum_required(VERSION 3.15)
project(MathglTest CXX)

find_package(MathGL REQUIRED)

option(WITH_QT "MathGL with qt5 enabled" OFF)
option(WITH_OPENGL "MathGL is opengl enabled" ON)

if(WITH_OPENGL)
  set(OpenGL_GL_PREFERENCE_LEGACY)
  find_package(OPENGL REQUIRED)
  message(STATUS "OPENGL_FOUND=${OPENGL_FOUND}")
  message(STATIS "OPENGL_LIBRARIES=${OPENGL_LIBRARIES}")
endif()

if(WITH_QT)
  find_package(Qt5 COMPONENTS Core Gui Widgets OpenGL REQUIRED)

  add_executable(qt_example qt_example.cpp)
  target_link_libraries(qt_example MathGL::MathGL Qt5::Core Qt5::Gui Qt5::Widgets Qt5::OpenGL)
  set(WITH_QT_TARGET "Qt5::Widgets")
endif()

add_executable(example example.cpp)
target_link_libraries(example MathGL::MathGL ${WITH_QT_TARGET} ${OPENGL_LIBRARIES})
