import pygame as py
import fileLoader
import math

class Fish:
    def __init__(self, posIn : list[int, int]):

        self.pos = posIn

        self.size = [188, 98]

        self.frame = 0

        self.images = [fileLoader.loadImage("fish/fish-0.png"),
                       fileLoader.loadImage("fish/fish-1.png"),
                       fileLoader.loadImage("fish/fish-2.png"),
                       fileLoader.loadImage("fish/fish-3.png"),
                       fileLoader.loadImage("fish/fish-4.png"),
                       fileLoader.loadImage("fish/fish-5.png")]

        self.collectedfish = False

        self.val = 0

    def draw(self, surfaceIn):
        if not self.collectedfish:
            surfaceIn.blit(self.images[self.frame], (self.pos[0], self.pos[1]))  # Corrected the blit method to use a tuple for position
            self.val += 1
            self.frame = math.floor(self.val/10) % 6


    def get(self) -> dict[str, int]:
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "w": self.size[0],
            "h": self.size[1],
            "collectedfish" : self.collectedfish
        }