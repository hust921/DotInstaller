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
        configs = {}

        # Parse software files
        for name in os.listdir(CONFIG_PATH):
            name = name.replace('.yaml', '')
            config = self.parse_config(name)
            if config is not None:
                configs[name] = config
                menu_soft = menu.add_menu_entry(MenuEntry(name))
                menu_soft.add_dependencies(config['dependencies'])

        # Show menu and question user for install
        menu_selection = menu.show_menu()
        if menu_selection is None:
            print("Quit. Nothing changed")
            exit(0)

        # Ask for dependencies
        print("Following packages will be installed: {0}".format(menu_selection['dependencies']))

        if input("Are you sure? [yes/No]: ") != 'yes':
            print("Installation cancelled. Nothing changed.")
            return

        # Ask for pre/post install edits
        for softname in menu_selection['software']:
            quit = False
            while not quit:
                print("\nInstall scripts [{0}]:".format(softname))
                print("\t1) Pre-Install")
                print("\t2) Post-Install")
                print("\t3) Continue")
                print("\t9) Cancel installation")
            
                choice = input("\n: ")
                if choice == "1":
                    print("NOT IMPLEMENTED!!!")
                    print("EDIT Pre-Install of: {0}, for debugging: {1}".format(softname, configs[softname]["pre-install"]))
                elif choice == "2":
                    print("NOT IMPLEMENTED!!!")
                    print("EDIT Post-Install of: {0}, for debugging: {1}".format(softname, configs[softname]["post-install"]))
                elif choice == "3":
                    quit = True
                elif choice == "9":
                    print("Installation cancelled. Nothing changed.")
                    exit(0)

        # Installation
        print("--------------------------------INSTALLING!--------------------------------")


    def __detect_python_version(self):
        '''Checks python version and exists in case of failure.'''
        if sys.version_info[0] < 3:
            print("Must be using python 3")
            exit(1)

    def parse_config(self, name):
        config = {}
        # Open file for parsing
        fpath = os.path.join(CONFIG_PATH, name) + '.yaml'
        with open(fpath, 'r') as f:
            conf = yaml.load(f)

        # If platform is specified, but not current one
        if 'platform' in conf and conf['platform'] != PLATFORM:
            return None
        # If distro is specified, but not current one
        if 'distro' in conf and conf['distro'] != DISTRO:
            return None

        # Pre-install
        if 'pre-install' in conf and conf['pre-install']:
            # If sorted by platform (windows/linux) and not null
            if PLATFORM in conf['pre-install']:
                config['pre-install'] = conf['pre-install'][PLATFORM]


        # Post-install
        if 'post-install' in conf and conf['post-install']:
            # If sorted by platform (windows/linux) and not null
            if PLATFORM in conf['post-install']:
                config['post-install'] = conf['post-install'][PLATFORM]


        # Install pakages
        if 'dependencies' in conf and conf['dependencies']:
            # If sorted by distrobution (windows/arch/debian)
            if DISTRO in conf['dependencies'] and conf['dependencies'][DISTRO]:
                config['dependencies'] = conf['dependencies'][DISTRO]

        return config


    def __run(self, cmds):
        # Determine if declared by distro
        if DISTRO in cmds:
            cmds = cmds[DISTRO]

        # Execute cmds
        for cmd in cmds:
            print("\t[CMD]: {0}".format(cmd))




if __name__ == '__main__':
    DepInstaller()
