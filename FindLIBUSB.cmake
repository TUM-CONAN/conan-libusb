find_path(LIBUSB_INCLUDE_DIR NAMES usb.h PATHS ${CONAN_INCLUDE_DIRS_LIBUSB})
find_library(LIBUSB_LIBRARY NAMES ${CONAN_LIBS_LIBUSB} PATHS ${CONAN_LIB_DIRS_LIBUSB})

set(LIBUSB_FOUND TRUE)
set(LIBUSB_INCLUDE_DIRS ${LIBUSB_INCLUDE_DIR})
set(LIBUSB_LIBRARIES ${LIBUSB_LIBRARY})
mark_as_advanced(LIBUSB_LIBRARY LIBUSB_INCLUDE_DIR)