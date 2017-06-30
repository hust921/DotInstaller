#!/usr/bin/python
'''
This is the main file for managing dotfile dependencies.
'''

import sys, os, yaml
from distutils.core import setup

from src.package_installer import PackageInstaller
from src.script_env import *

class DepInstaller:
    def __init__(self):
        '''Interactive configuration menu for dotfiles.
        Run this script without any arguments to get access to
        interactive menu.
        '''
        self.__detect_python_version()
        self.pkgman = PackageInstaller(DISTRO)

        # Parse software files
        for name in os.listdir(SOFTWARE_CONFIGS):
            self.__config_install(name, os.path.join(SOFTWARE_CONFIGS, name))

        # Parse distro files
        for name in os.listdir(PKG_CONFIGS):
            self.__config_install(name, os.path.join(PKG_CONFIGS, name))


    def __detect_python_version(self):
        '''Checks python version and exists in case of failure.'''
        if sys.version_info[0] < 3:
            print("Must be using python 3")
            exit(1)

    def __config_install(self, name, configFile):
        '''Install software/packages using information stored in
        configFile (.yaml full path).
        '''
        print("--------------------------------")
        print("[{0}] Installing..".format(name))

        with open(configFile, 'r') as f:
            conf = yaml.load(f)
            
            # Pre-install
            print("-----\n[{0}] Pre-install..".format(name))
            # If any pre-install cmds/instructions
            if 'pre-install' in conf and conf['pre-install']:

                # If sorted by platform (windows/linux) and not null
                cmds = conf['pre-install']
                if PLATFORM in conf['pre-install']:
                    cmds = cmds[PLATFORM]

                self.__run(cmds)

            # Install pakages
            print("-----\n[{0}] Dependencies..".format(name))
            # If any dependencies
            if 'dependencies' in conf and conf['dependencies']:
                
                # If sorted by distrobution (windows/arch/debian)
                # And not null
                deps = conf['dependencies']
                if DISTRO in conf and conf[DISTRO]:
                    deps = deps[DISTRO]

                self.pkgman.install(deps)

            # Post-install
            print("-----\n[{0}] Post-install..".format(name))
            # If any post-install cmds/instructions
            if 'post-install' in conf and conf['post-install']:

                # If sorted by platform (windows/linux) and not null
                cmds = conf['post-install']
                if PLATFORM in conf['post-install']:
                    cmds = cmds[PLATFORM]

                self.__run(cmds)
    

    def __run(self, cmds):
        # Determine if declared by distro
        if DISTRO in cmds:
            cmds = cmds[DISTRO]

        # Execute cmds
        for cmd in cmds:
            print("\t[CMD]: {0}".format(cmd))




if __name__ == '__main__':
    installer = DepInstaller()
