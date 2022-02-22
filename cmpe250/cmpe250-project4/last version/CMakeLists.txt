cmake_minimum_required(VERSION 2.8.2.12)
project(project4)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")

set(SOURCE_FILES main.cpp Node.cpp Node.h Simulation.cpp Simulation.h)
add_executable(project4 ${SOURCE_FILES})