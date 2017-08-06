#!/usr/bin/python
'''
This is the main file for managing dotfile dependencies.
'''

import sys, os, yaml
from distutils.core import setup

from src.package_installer import PackageInstaller
from src.script_env import *
from src.script_editor import ScriptEditor
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

        # Find configs for selected software in menu
        selected_confs = {}
        for soft in menu_selection['software']:
            selected_confs[soft] = configs[soft]

        # Ask for pre/post install edits
        sedit = ScriptEditor()
        sedit.show_menu(selected_confs)

        # Installation
        print("--------------------------------INSTALLING!--------------------------------")
        print(menu_selection['dependencies'])
        print("----")
        print(selected_confs)


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
