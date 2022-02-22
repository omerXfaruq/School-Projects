cmake_minimum_required(VERSION 2.8.2.12)
project(Cmpe250_Project2)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp Person.cpp Person.h Simulation.cpp Simulation.h)
add_executable(Cmpe250_Project2 ${SOURCE_FILES})