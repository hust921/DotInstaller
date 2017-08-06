#!/usr/bin/python 

import os, subprocess, tempfile

class ScriptEditor:
    '''Shows menu user to edit pre- and post- install scripts.
    Add configs to the editor and run 'show_menu' to ask user.
    '''

    def __init__(self):
        pass


    def show_menu(self, configs):
        '''Shows interactive menu to user for him/her to edit scripts.
        configs arg is a dictionary where the key is the name
        of the software and value is another dictionary.
        Using keys 'pre-install' and 'post-install' with arrays
        of commands to execute
        '''

        # Iterate dictionary
        for key in configs:

            config = configs[key]
            # Loop menu until 'continue' is selected
            quit = False
            while not quit:
                print("\nInstall scripts [{0}]:".format(key))
                print("\t1) Edit Pre-Install")
                print("\t2) Edit Post-Install")
                print("\t3) Continue")
                print("\t9) Cancel installation")

                choice = input("\n: ")
                if choice == '1':
                    config['pre-install'] = self.__edit_install(config['pre-install'])

                elif choice == '2':
                    config['post-install'] = self.__edit_install(config['post-install'])

                elif choice == '3':
                    quit = True

                elif choice == '9':
                    print("Installation cancelled. Nothing changed.")
                    exit(0)


    def __edit_install(self, cmdlist):
        '''Edit list of commands using native terminal editor.'''

        # Create, edit, parse and unlink temp file
        filepath = self.__create_tmp_file(cmdlist)
        self.__open_native_editor(filepath)
        cmdlist = self.__parse_script_file(filepath)
        os.remove(filepath)

        return cmdlist


    def __create_tmp_file(self, cmds):
        '''Creates temp file containing the array of commands parsed
        as separate lines for each entry. Returns full filepath to 
        the new temp file.
        '''
        # Create file and write cmds
        fd, fname = tempfile.mkstemp()
        with open(fname, 'w') as f:
            for cmd in cmds:
                f.write("{line}{newline}".format(line=cmd, newline=os.linesep))

        os.close(fd)
        return fname

    def __open_native_editor(self, filepath):
        '''Opens file with native EDITOR (env var) or vi.'''
        # Find default editor & construct command
        cmd = os.environ.get('EDITOR', 'vi')
        cmd = cmd + ' ' + filepath

        # Open for editing
        subprocess.call(cmd, shell=True)

    def __parse_script_file(self, filepath):
        '''Parses every line in file as entries in array.'''
        cmds = None
        with open(filepath) as f:
            cmds = f.read().splitlines()

        return cmds

