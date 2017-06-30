#!/usr/bin/python
'''
This is the main file for managing dotfile dependencies.
'''

import sys, os, yaml
from distutils.core import setup

from src.package_installer import PackageInstaller
from src.script_env import *
from src.runner import Runner

class DepInstaller:
    def __init__(self):
        '''Interactive configuration menu for dotfiles.
        Run this script without any arguments to get access to
        interactive menu.
        '''
        self.__detect_python_version()
        self.runner = Runner(PLATFORM)
        self.pkgman = PackageInstaller(DISTRO)

        # Parse software files
        for soft in os.listdir(SOFTWARE_CONFIGS):
            self.__install_software(soft)

    def install(self):
        pass


    def __detect_python_version(self):
        '''Checks python version and exists in case of failure.'''
        if sys.version_info[0] < 3:
            print("Must be using python 3")
            exit(1)

    def __install_software(self, soft):
        '''Install software using information stored in yaml config
        file. Passed as: soft
        '''
        with open(os.path.join(SOFTWARE_CONFIGS, soft), 'r') as f:
            soft = yaml.load(f)
            
            # Pre-install
            if soft['pre-install']:
                self.runner.run(soft['pre-install'][PLATFORM])

            # Install pakages
            if soft['dependencies']:
                self.pkgman.install(soft['dependencies'][DISTRO])

            # Post-install
            if soft['post-install']:
                self.runner.run(soft['post-install'][PLATFORM])



if __name__ == '__main__':
    installer = DepInstaller()
    installer.install()
