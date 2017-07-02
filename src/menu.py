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

    def add_dependency(self, dep, selected=True):
        self.__deps.append((selected, dep))

    def add_dependencies(self, deps, selected=True):
        for dep in deps:
            self.__deps.append((selected, dep))

    def remove_dependency(self, dep):
        self.__deps.remove(dep)

    def get_dependencies(self):
        return self.__deps

    def n_dependencies(self):
        return len(self.__deps)

    def change_select(self, dep, selected=None):
        for i, d in enumerate(self.__deps):
            if d == dep:

                if selected is None:
                    selected = not dep[0]
                self.__deps[i] = (selected, dep[1])


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
                    if d[0]:
                        dependencies.append(d[1])

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
        self.stdscr.addstr(2, 5, "Platform: " + PLATFORM)
        self.stdscr.addstr(2, 45, "(i)nstall")
        self.stdscr.addstr(3, 5, "pkg-man: " + PKGMAN + " "+ PKGMAN_OPTIONS)
        self.stdscr.addstr(3, 45, "(s)elect")

        # Add menu entries
        line = self.y
        for entry in self.__entries:
            sep = "-" * int((curses.COLS/2) - len(entry.text) - 5)
            msg = "[{1}] {0} {2}\n".format(entry.text, xselect(entry.selected), sep)
            self.stdscr.addstr(line, 0, msg)
            self.__menu_lower += 1
            line += 1

            # Add dependencies
            for (selected, dep) in entry.get_dependencies():
                self.stdscr.addstr(line, 0, "\t[{1}] {0}\n".format(dep, xselect(selected)))
                self.__menu_lower += 1
                line += 1

        self.stdscr.refresh()
        self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
        self.stdscr.move(self.y, self.x)

    def __refresh_menu(self):
        # Add menu entries
        line = self.__menu_upper
        for entry in self.__entries:
            sep = "-" * int((curses.COLS/2) - len(entry.text) - 5)
            msg = "[{1}] {0} {2}\n".format(entry.text, xselect(entry.selected), sep)
            self.stdscr.addstr(line, 0, msg)
            line += 1

            # Add dependencies
            for (selected, dep) in entry.get_dependencies():
                self.stdscr.addstr(line, 0, "\t[{1}] {0}\n".format(dep, xselect(selected)))
                line += 1

        self.stdscr.refresh()
        self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
        self.stdscr.move(self.y, self.x)


    def __user_input(self):
        stdscr = self.stdscr # For readability
        while True:
            key = stdscr.getkey()

            if key == 'q':
                return False

            # Up key AND inside menu window bounds
            elif (key == 'KEY_UP' or key == 'k') and self.y > self.__menu_upper:
                self.stdscr.chgat(self.y, 0, curses.A_NORMAL)
                self.y -= 1
                self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
                self.stdscr.move(self.y, self.x)

            # Down key AND inside menu window bounds
            elif (key == 'KEY_DOWN' or key == 'j') and self.y < self.__menu_lower:
                self.stdscr.chgat(self.y, 0, curses.A_NORMAL)
                self.y += 1
                self.stdscr.chgat(self.y, 0, curses.A_STANDOUT)
                self.stdscr.move(self.y, self.x)

            elif key == 'i':
                return True

            elif key == 's':
                self.__change_select(self.y - self.__menu_upper)


    def __change_select(self, n):
        i = 0
        f = open("installer.log", 'a+')
        for e in self.__entries:
            if n == i:
                e.selected = not e.selected
                for d in e.get_dependencies():
                    f.write("({0}) (i:{1}) found it\n".format(n, i))
                    e.change_select(d, selected=e.selected)
                    i += 1
                self.__refresh_menu()
                return

            elif n > i + e.n_dependencies():
                f.write("({0}) (i:{1}) not yet\n".format(n, i))
                i += e.n_dependencies()

            else:
                for d in e.get_dependencies():
                    i += 1
                    f.write("({0}) (i:{1}) inside\n".format(n, i))
                    if i == n:
                        e.change_select(d)
                        self.__refresh_menu()
                        return
            i += 1



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

