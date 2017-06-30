#!/usr/bin/python
import platform

class PackageInstaller:
    def __init__(self):
        __detect_os(self)


    def install(self, packages):
        pass


    def __detect_os(self):
        # Windows
        if platform.system() == 'Windows':
            self.platform = 'win'
            self.os = 'win'
            self.pkgman = 'chocolatey'
            self.pkgman_flags = ''
            return

        # Linux Distrobutions
        elif platform.system() == 'Linux':
            self.platform = 'linux'

            # Arch linux
            if platform.linux_distribution()[0] == 'arch':
                self.os = 'arch'
                self.pkgman = 'apacman'
                self.pkgman_flags = ' -Sy '

            # Debian
            if platform.linux_distribution()[0] == 'debian':
                self.os = 'debian'
                self.pkgman = 'apt-get'
                self.pkgman_flags = ' install -y '
