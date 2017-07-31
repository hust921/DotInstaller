#!/usr/bin/python
'''Contains information about enviroment for installation.'''
import os, platform

def __get_script_dir():
    return os.path.dirname(os.path.dirname(__file__))


def __get_dotfiles_dir():
    envfile = os.path.dirname(os.path.dirname(__file__))
    return os.path.dirname(envfile)


def __detect_os():
    # Windows
    if platform.system() == 'Windows':
        plat = 'windows'
        distro = 'windows'
        pkgman = 'exit; echo "WIN NOT IMPLEMENTED!"'

    # Linux Distrobutions
    elif platform.system() == 'Linux':
        plat = 'linux'

        # Arch linux
        if platform.linux_distribution()[0] == 'arch':
            distro = 'arch'
            pkgman = 'apacman'
            options = '-S'

        # Debian
        elif platform.linux_distribution()[0] == 'debian':
            distro = 'debian'
            pkgman = 'apt-get'
            options = 'install'

    # Failed to detect os
    else:
        print("ERROR! Failed to detect platform/distro system..")
        exit(2)

    return (plat, distro, pkgman, options)

DOTFILES_DIR = __get_dotfiles_dir()
SCRIPT_DIR   = __get_script_dir()
CONFIG_PATH   = os.path.join(SCRIPT_DIR, 'configs')
PLATFORM, DISTRO, PKGMAN, PKGMAN_OPTIONS = __detect_os()
