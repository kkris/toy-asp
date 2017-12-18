from enum import Enum


class Level(Enum):
    DEBUG = 0
    INFO = 1
    NONE = 2


global_level = Level.DEBUG


def set_level(level):
    global global_level
    global_level = level


class Logger(object):

    def __init__(self, level=None):
        if level is None:
            self.level = global_level
        else:
            self.level = level

    def set_level(self, level):
        self.level = level

    def log(self, s, level):
        if level.value >= self.level.value:
            print("[" + level.name + "]\t" + s)

    def debug(self, s):
        self.log(s, Level.DEBUG)

    def info(self, s):
        self.log(s, Level.INFO)
