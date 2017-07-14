#!/usr/bin/python
import os
from src.script_env import *
import curses

def xselect(selected):
    return 'x' if selected else ' '

class MenuEntry:
    def __init__(self, text, selected=True):
        self.text = text
        self.selected = selected
        self.__deps = []
        self.exspanded = False

    def add_dependency(self, dep, selected=True):
        self.__deps.append({'selected': selected, 'name': dep})

    def add_dependencies(self, deps, selected=True):
        for dep in deps:
            self.__deps.append({'selected': selected, 'name': dep})

    def remove_dependency(self, dep):
        self.__deps.remove(dep)

    def get_dependencies(self):
        return self.__deps

    def n_dependencies(self):
        return len(self.__deps)


class Menu:
    '''Simple dynamic interactive menu.'''


    def __init__(self):
        self.__entries = []
        # Cursor possition


    def add_menu_entry(self, menuEntry):
        '''Adds entry to menu enties.'''
        self.__entries.append(menuEntry)
        return menuEntry


    def remove_menu_entry(self, *, index=-1, entry=None):
        '''Removes entry from menu by index or reference.
        Both are forced (*) to use keyword.
        If BOTH are supplied, "entry" is used.
        '''

        # Check arguments
        if index == -1 and entry == None:
            raise Exception("""Only args: "index" OR "entry" can be set.
                            When calling MenuEntry.remove_menu_entry()""")

        # if index given
        if entry == None:
            entry = self.__entries[index]

        # Remove
        self.__entries.remove(entry)


    def show_menu(self):
        # Init curses
        self.__curses_init()

        # Draw menu and wait for user
        self.__draw_menu()
        install = self.__user_input()

        # Remember to cleanup
        self.__curses_cleanup()

        # Collect dependencies if not cancelled
        if install:
            dependencies = []
            for e in self.__entries:
                for d in e.get_dependencies():
                    if d['selected']:
                        dependencies.append(d['name'])

            return dependencies
        else:
            return None


    def __draw_menu(self):
        # Menu bounderies
        self.__menu_upper = 6
        self.__menu_lower = 5

        # Draw menu header
        self.stdscr.addstr(' ' * curses.COLS)
        msg = "Dofiles installer - <Morten Lund>"
        empty = " " * int((curses.COLS/2) - (len(msg)/2))
        msg = empty + msg + empty
        self.stdscr.addstr(0, 0, msg, curses.A_STANDOUT)

        # Draw options
        self.stdscr.addstr(1, 5, "Distro: " + DISTRO)
        self.stdscr.addstr(1, 45, "(q)uit")
        self.stdscr.addstr(1, 65, "(e)xspand")
        self.stdscr.addstr(2, 5, "Platform: " + PLATFORM)
        self.stdscr.addstr(2, 45, "(i)nstall")
        self.stdscr.addstr(3, 5, "pkg-man: " + PKGMAN + " "+ PKGMAN_OPTIONS)
        self.stdscr.addstr(3, 45, "(s)elect")

        # Refresh menu
        self.__refresh_menu()


    def __refresh_menu(self):
        self.__menu_lower = self.__menu_upper-1
        # Add menu entries
        line = self.__menu_upper
        for entry in self.__entries:
            sep = "-" * int((curses.COLS/2) - len(entry.text) - 5)
            msg = "[{1}] {0} {2}\n".format(entry.text, xselect(entry.selected), sep)
            self.stdscr.addstr(line, 0, msg)
            self.__menu_lower += 1
            line += 1

            if entry.exspanded:
                # Add dependencies
                for dep in entry.get_dependencies():
                    if (line < curses.LINES-1):
                        self.stdscr.addstr(line, 0, "\t[{1}] {0}\n".format(dep['name'], xselect(dep['selected'])))
                        self.__menu_lower += 1
                        line += 1

        # Clear lines after menu
        while (line < curses.LINES-1):
            self.stdscr.addstr(line, 0, ' '*curses.COLS)
            line += 1

        self.stdscr.refresh()
        self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
        self.stdscr.move(self.y, self.x)


    def __user_input(self):
        stdscr = self.stdscr # For readability
        while True:
            key = stdscr.getkey()

            # g/G vim bindings
            if key == 'g':
                key = stdscr.getkey()
                if key == 'g':
                    self.__move_cursor(self.__menu_upper, self.x)

            if (key == 'G'):
                    self.__move_cursor(self.__menu_lower, self.x)

            # Regular keybindings
            elif key == 'q':
                return False

            # Up key AND inside menu window bounds
            elif (key == 'KEY_UP' or key == 'k') and self.y > self.__menu_upper:
                self.__move_cursor(self.y-1, self.x)

            # Down key AND inside menu window bounds
            elif (key == 'KEY_DOWN' or key == 'j') and self.y < self.__menu_lower:
                self.__move_cursor(self.y+1, self.x)

            elif key == 'i':
                return True

            elif key == 's' or key == ' ':
                entry = self.__entry_under_cursor()
                
                # Change all dependencies
                if (type(entry) is MenuEntry):
                    entry.selected = not entry.selected
                    for d in entry.get_dependencies():
                        d['selected'] = entry.selected
                # Change dependency
                else:
                    entry['selected'] = not entry['selected']
                self.__refresh_menu()

            elif key == 'e':
                # Find entry selected
                entry = self.__entry_under_cursor()

                # Change exspanded/collapsed
                if (type(entry) is MenuEntry):
                    entry.exspanded = not entry.exspanded
                    self.__refresh_menu()


    def __entry_under_cursor(self):
        '''Returns MenuEntry for menu entry
        or (selected, dep) for dependency
        under the cursor.
        '''
        i = 0
        n = self.y - self.__menu_upper

        # Loop main menu entries
        for e in self.__entries:
            # If cursor is beyond a main menu entry,
            # skip entire entry. (only count if expanded)
            if n > i + e.n_dependencies() and e.exspanded:
                i += e.n_dependencies()

            # If main entry return
            elif n == i:
                return e

            # Else dependency of current (main menu) entry was selected.
            # (only count if expanded)
            elif e.exspanded:
                for d in e.get_dependencies():
                    i += 1
                    if i == n:
                        return d
            i += 1
        raise Exception("Failed to find menu entry or dependency selected.\
                In Menu.__entry_under_cursor()")


    def __move_cursor(self, y, x):
        self.stdscr.chgat(self.y, 0, curses.A_NORMAL)
        self.y = y
        self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
        self.stdscr.move(self.y, self.x)


    def __get_menu_entries(self):
        '''Returns all main menu entries.'''
        return self.__entries
    

    def __curses_init(self):
        # init curses
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Cusor possition
        self.y = 6
        self.x = curses.COLS - 1



    def __curses_cleanup(self):
        curses.curs_set(1)
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

