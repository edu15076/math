################################################################################
### Selecting CMake minimum version

cmake_minimum_required(VERSION 3.9)

################################################################################
### Setting Global Parameters

set(PROJECT_NAME "Playground")
set(BINARY_NAME "playground")

project("${PROJECT_NAME}")

set(CMAKE_CXX_STANDARD 20)

include(GNUInstallDirs)

SET(APP_BASE_PATH "${PROJECT_SOURCE_DIR}/code")

SET(THREADS_PREFER_PTHREAD_FLAG ON)
FIND_PACKAGE(Threads REQUIRED)

################################################################################
### Project definition

INCLUDE(CheckIncludeFile)

include_directories(
        "${APP_BASE_PATH}/"
)

FILE(
        GLOB SOURCES
        "${APP_BASE_PATH}/*.cpp"
)

LINK_DIRECTORIES(
        "/usr/local/lib/"
)

ADD_DEFINITIONS("-g")

ADD_EXECUTABLE (
        ${BINARY_NAME} ${SOURCES}
)

TARGET_LINK_LIBRARIES(${BINARY_NAME} PUBLIC "math")
