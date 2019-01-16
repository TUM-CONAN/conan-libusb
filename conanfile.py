from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibusbConan(ConanFile):
    name = "libusb"
    version = "1.0.22"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = ["FindUSB.cmake"]
    exports = [
    ]
    url = "https://git.ircad.fr/conan/conan-libusb"
    license="LGPL"
    description = "A cross-platform library to access USB devices"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = True

    def configure(self):
        del self.settings.compiler.libcxx
        if 'CI' not in os.environ:
            os.environ["CONAN_SYSREQUIRES_MODE"] = "verify"

    def source(self):
        if tools.os_info.is_macos:
            tools.get("https://github.com/libusb/libusb/archive/v{0}.zip".format(self.version))
            os.rename("libusb-{0}".format(self.version), self.source_subfolder)

    def build(self):
        if tools.os_info.is_macos:
            libusb_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        
            with tools.chdir(libusb_source_dir):                
                autotools = AutoToolsBuildEnvironment(self)
                with tools.environment_append(autotools.vars):
                    self.run("chmod +x *.sh && ./autogen.sh")

                autotools.fpic = self.options.shared
                autotools.configure()
                autotools.make()
                autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.copy("FindUSB.cmake", ".", ".")
