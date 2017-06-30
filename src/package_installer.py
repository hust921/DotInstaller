#!/usr/bin/python

class PackageInstaller:
    def __init__(self, distro, pkgman):
        self.distro = distro
        self.pkgman = pkgman


    def install(self, deps):
        # installing deps
        installcmd = "\t[DEP]: {0} {1}".format(self.pkgman, ' '.join(deps))
        print(installcmd)
