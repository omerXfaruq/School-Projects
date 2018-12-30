cmake_minimum_required(VERSION 2.8.2.12)
project(project4)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 ")

set(SOURCE_FILES main.cpp )
add_executable(project5 ${SOURCE_FILES})