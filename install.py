#!/usr/bin/python
'''
This is the main file for managing dotfile dependencies.
'''

import sys
from distutils.core import setup
from src.package_manager import PackageManager

class DepInstaller:
    def __init__(self):
        '''Interactive configuration menu for dotfiles.
        Run this script without any arguments to get access to
        interactive menu.
        '''
        self.detect_python_version()

    def install(self):
        pass


    def detect_python_version(self):
        '''Checks python version and exists in case of failure.'''
        if sys.version_info[0] < 3:
            print("Must be using python 3")
            exit(1)

if __name__ == '__main__':
    installer = DepInstaller()
    installer.install()
