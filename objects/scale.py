import pygame as py
import fileLoader
import math

class Scale:
    def __init__(self, posIn: list[int, int]):

        self.pos = posIn

        self.images = [fileLoader.loadImage("scale-0.png"),
                       fileLoader.loadImage("scale-1.png"),
                       fileLoader.loadImage("scale-2.png"),
                       fileLoader.loadImage("scale-3.png"),
                       fileLoader.loadImage("scale-4.png"),
                       fileLoader.loadImage("scale-5.png"),
                       fileLoader.loadImage("scale-6.png"),
                       fileLoader.loadImage("scale-7.png"),
                       fileLoader.loadImage("scale-8.png"),
                       fileLoader.loadImage("scale-9.png"),
                       fileLoader.loadImage("scale-10.png"),
                       fileLoader.loadImage("scale-11.png")]

        self.size = [80, 183]

        self.frame = 0

        self.collected = False

        self.val = 0

    def draw(self, surfaceIn):
        surfaceIn.blit(self.images[self.frame], (self.pos[0], self.pos[1]-20))  # Corrected the blit method to use a tuple for position
        self.val += 1
        self.frame = math.floor(self.val / 10) % 11


    def get(self) -> dict[str, int]:
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "w": self.size[0],
            "h": self.size[1],
            "collected" : self.collected
        }
    def collect(self):
        self.collected = True