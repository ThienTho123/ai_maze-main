import configparser

from config.config import *


class Config:
    def __init__(self, width=INIT_WIDTH, height=INIT_HEIGHT, level=1):
        self.startcolor = STARTCOLOR
        self.visitedcolor = VISITEDCOLOR
        self.bordercolor = BORDERCOLOR
        self.maincolor = MAINCOLOR
        self.width, self.height = width, height
        self.fps = FPS
        self.level = level
        self.ratio = 1
        self.cellsize = self.cellsize_ratio()
        self.Visualization_speed = Visualization_speed

    def cellsize_level(self):
        cellsize = CELLSIZE
        if self.level != 1:
            cell = self.height // CELLSIZE + 5 * self.level
            cellsize = self.height // cell
        return cellsize

    def cellsize_ratio(self, ratio=None):
        if ratio is None:
            ratio = self.ratio
        self.cellsize = self.cellsize_level() * ratio
        return self.cellsize

    def set_level(self, level):
        self.level = level
        self.cellsize = self.cellsize_ratio()
    def config_load(self):
        config = configparser.ConfigParser()
        config.read('config/config.ini')

    def config_save(self):
        config = configparser.ConfigParser()
        config.read('config/config.ini')

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
