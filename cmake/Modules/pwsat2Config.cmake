INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PWSAT2 pwsat2)

FIND_PATH(
    PWSAT2_INCLUDE_DIRS
    NAMES pwsat2/api.h
    HINTS $ENV{PWSAT2_DIR}/include
        ${PC_PWSAT2_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PWSAT2_LIBRARIES
    NAMES gnuradio-pwsat2
    HINTS $ENV{PWSAT2_DIR}/lib
        ${PC_PWSAT2_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PWSAT2 DEFAULT_MSG PWSAT2_LIBRARIES PWSAT2_INCLUDE_DIRS)
MARK_AS_ADVANCED(PWSAT2_LIBRARIES PWSAT2_INCLUDE_DIRS)

