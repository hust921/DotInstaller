#!/usr/bin/python

class PackageInstaller:
    def __init__(self, distro):
        self.distro = distro


    def install(self, deps):
        # installing deps
        for d in deps:
            print("\t[DEP]: {0}".format(d))
