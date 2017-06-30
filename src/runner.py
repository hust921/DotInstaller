#!/usr/bin/python

class Runner:
    def __init__(self, platform):
        self.platform = platform

    def run(self, cmds):
        print("RUNNING cmds: " + str(cmds))
