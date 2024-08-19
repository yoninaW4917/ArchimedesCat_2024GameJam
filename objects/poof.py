import fileLoader
import pygame

class Poof:
    def __init__(self, posIn : list[int, int]):

        self.pos = posIn

        self.size = [188, 98]

        self.frame = 0

        self.images_med = [fileLoader.loadImage("mPoof/mPoof-0"),
                           fileLoader.loadImage("mPoof/mPoof-1"),
                           fileLoader.loadImage("mPoof/mPoof-2"),
                           fileLoader.loadImage("mPoof/mPoof-3"),
                           fileLoader.loadImage("mPoof/mPoof-4")]

        self.val = 0