import pygame as py
import fileLoader
import math

class Scale:
    def __init__(self, posIn: list[int, int]):

        self.pos = posIn

        self.images = [fileLoader.loadImage("scale/scale-0.png"),
                       fileLoader.loadImage("scale/scale-1.png"),
                       fileLoader.loadImage("scale/scale-2.png"),
                       fileLoader.loadImage("scale/scale-3.png"),
                       fileLoader.loadImage("scale/scale-4.png"),
                       fileLoader.loadImage("scale/scale-5.png"),
                       fileLoader.loadImage("scale/scale-6.png"),
                       fileLoader.loadImage("scale/scale-7.png"),
                       fileLoader.loadImage("scale/scale-8.png"),
                       fileLoader.loadImage("scale/scale-9.png"),
                       fileLoader.loadImage("scale/scale-10.png"),
                       fileLoader.loadImage("scale/scale-11.png")]

        self.size = [80, 183]

        self.frame = 0

        self.collected = False

        self.val = 0

    def draw(self, surfaceIn):
        if not self.collected:
            surfaceIn.blit(self.images[self.frame], (self.pos[0], self.pos[1]-20))  # Corrected the blit method to use a tuple for position
            self.val += 1
            self.frame = math.floor(self.val / 10) % 11

    def reset(self):
        self.collected = False
        self.val = 0
        self.frame = 0

    def get(self) -> dict[str, int]:
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "w": self.size[0],
            "h": self.size[1],
            "collected" : self.collected
        }