from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibusbConan(ConanFile):
    name = "libusb"
    package_revision = "-r1"
    upstream_version = "1.0.22"
    version = "{0}{1}".format(upstream_version, package_revision)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = [
        'FindUSB.cmake',
        'FindLIBUSB.cmake'
    ]
    exports = [
    ]
    url = "https://git.ircad.fr/conan/conan-libusb"
    license="LGPL"
    description = "A cross-platform library to access USB devices"
    source_subfolder = "source_subfolder"
    compat_source = "compat_source"
    build_subfolder = "build_subfolder"
    short_paths = True

    def configure(self):
        del self.settings.compiler.libcxx
        if 'CI' not in os.environ:
            os.environ["CONAN_SYSREQUIRES_MODE"] = "verify"

    def source(self):
        if tools.os_info.is_macos:
            tools.get("https://github.com/libusb/libusb/archive/v{0}.zip".format(self.upstream_version))
            os.rename("libusb-{0}".format(self.upstream_version), self.source_subfolder)

            tools.get("https://github.com/libusb/libusb-compat-0.1/archive/v0.1.7.tar.gz")
            os.rename("libusb-compat-0.1-0.1.7", self.compat_source)

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

            compat_source_dir = os.path.join(self.source_folder, self.compat_source)

            with tools.chdir(compat_source_dir):                
                autotools = AutoToolsBuildEnvironment(self)
                with tools.environment_append(autotools.vars):
                    with tools.environment_append({"PKG_CONFIG_PATH": os.path.join(self.package_folder, 'lib', 'pkgconfig')}):
                        self.run("chmod +x *.sh && ./autogen.sh")

                        autotools.fpic = self.options.shared
                        autotools.configure()
                        autotools.make()
                        autotools.install()

    def package(self):
        self.copy("FindUSB.cmake", ".", ".", keep_path=False)
        self.copy("FindLIBUSB.cmake", ".", ".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        
