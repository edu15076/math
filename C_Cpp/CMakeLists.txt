################################################################################
### Selecting CMake minimum version

cmake_minimum_required(VERSION 3.9)

################################################################################
### Setting Global Parameters

set(PROJECT_NAME "Math")
set(BINARY_NAME "math")

project("${PROJECT_NAME}")

set(LIBRARY_VERSION_MAJOR 0)
SET(LIBRARY_VERSION_STRING 0.1)

set(CMAKE_CXX_STANDARD 20)

include(GNUInstallDirs)

set(LIBRARY_BASE_PATH "${PROJECT_SOURCE_DIR}/code")

set(LIBRARY_PUBLIC_PATH "${LIBRARY_BASE_PATH}/public")

set(LIBRARY_PUBLIC_SOURCES_PATH "${LIBRARY_PUBLIC_PATH}/src")

set(LIBRARY_PUBLIC_HEADERS_PATH "${LIBRARY_PUBLIC_PATH}/include")

################################################################################
### Project definition

include_directories(
        "${LIBRARY_BASE_PATH}"
)

set(PUBLIC_SOURCE_FILES
        "${LIBRARY_PUBLIC_SOURCES_PATH}/exp.cpp"
        "${LIBRARY_PUBLIC_SOURCES_PATH}/pow.cpp"
        "${LIBRARY_PUBLIC_SOURCES_PATH}/PrimeUtils.cpp"
)

set(PUBLIC_HEADERS_FILES
        "${LIBRARY_PUBLIC_HEADERS_PATH}/math.hpp"
)

set(CMAKE_CXX_VISIBILITY_PRESET hidden)

add_library(
        ${BINARY_NAME} SHARED ${PUBLIC_SOURCE_FILES}
)

set_target_properties(
        ${BINARY_NAME} PROPERTIES
        VERSION		  ${LIBRARY_VERSION_STRING}
        SOVERSION	  ${LIBRARY_VERSION_MAJOR}
        PUBLIC_HEADER ${PUBLIC_HEADERS_FILES}
)

################################################################################
### Adding compilator definitions, like debug symbols

add_definitions("-g")

################################################################################
### Library installation directives

install(
        TARGETS 					${BINARY_NAME}
        LIBRARY DESTINATION			${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION	${CMAKE_INSTALL_INCLUDEDIR}
)
