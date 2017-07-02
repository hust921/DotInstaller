#!/usr/bin/python
'''
This is the main file for managing dotfile dependencies.
'''

import sys, os, yaml
from distutils.core import setup

from src.package_installer import PackageInstaller
from src.script_env import *
from src.menu import Menu, MenuEntry

class DepInstaller:
    def __init__(self):
        '''Interactive configuration menu for dotfiles.
        Run this script without any arguments to get access to
        interactive menu.
        '''
        self.__detect_python_version()
        self.pkgman = PackageInstaller(DISTRO, PKGMAN)
        menu = Menu()

        # Parse software files
        for name in os.listdir(SOFTWARE_CONFIGS):
            name = name.replace('.yaml', '')
            menu_soft = menu.add_menu_entry(MenuEntry(name))
            packages = self.parse_soft_config(name)['dependencies']
            menu_soft.add_dependencies(packages)


        # Parse distro files
        menu_pkg = menu.add_menu_entry(MenuEntry("{0} ({1}):".format(str(DISTRO), str(PKGMAN))))
        for name in os.listdir(PKG_CONFIGS):
            name = name.replace('.yaml', '')
            if name == PKGMAN:
                packages = self.parse_pkg_config(name)['dependencies']
                menu_pkg.add_dependencies(packages)

        packages = menu.show_menu()
        if packages is None:
            print("Quit. Nothing changed")
        else:
            print("Following packages will be installed: {0}".format(packages))

            while True:
                answer = input("Are you sure? [yes/No]: ") 

                if answer == 'yes':
                    print("--------------------------------INSTALLING!--------------------------------")
                    return

                elif answer.lower() == 'no' or answer.lower() == 'n':
                    print("Installation cancelled. Nothing changed.")
                    return


    def __detect_python_version(self):
        '''Checks python version and exists in case of failure.'''
        if sys.version_info[0] < 3:
            print("Must be using python 3")
            exit(1)


    def parse_pkg_config(self, name):
        pkg = {}
        fpath = os.path.join(PKG_CONFIGS, name) + '.yaml'
        with open(fpath, 'r') as f:
            conf = yaml.load(f)

        # Pre-install
        if 'pre-install' in conf and conf['pre-install']:
            pkg['pre-install'] = conf['pre-install']

        # Post-install
        if 'post-install' in conf and conf['post-install']:
            pkg['post-install'] = conf['post-install']

        # Dependencies
        if 'dependencies' in conf and conf['dependencies']:
            pkg['dependencies'] = conf['dependencies']

        return pkg


    def parse_soft_config(self, name):
        soft = {}
        fpath = os.path.join(SOFTWARE_CONFIGS, name) + '.yaml'
        with open(fpath, 'r') as f:
            conf = yaml.load(f)

        # Pre-install
        if 'pre-install' in conf and conf['pre-install']:
            # If sorted by platform (windows/linux) and not null
            if PLATFORM in conf['pre-install']:
                soft['pre-install'] = conf['pre-install'][PLATFORM]


        # Post-install
        if 'post-install' in conf and conf['post-install']:
            # If sorted by platform (windows/linux) and not null
            if PLATFORM in conf['post-install']:
                soft['post-install'] = conf['post-install'][PLATFORM]


        # Install pakages
        if 'dependencies' in conf and conf['dependencies']:
            # If sorted by distrobution (windows/arch/debian)
            if DISTRO in conf['dependencies'] and conf['dependencies'][DISTRO]:
                soft['dependencies'] = conf['dependencies'][DISTRO]

        return soft


    def __run(self, cmds):
        # Determine if declared by distro
        if DISTRO in cmds:
            cmds = cmds[DISTRO]

        # Execute cmds
        for cmd in cmds:
            print("\t[CMD]: {0}".format(cmd))




if __name__ == '__main__':
    installer = DepInstaller()
