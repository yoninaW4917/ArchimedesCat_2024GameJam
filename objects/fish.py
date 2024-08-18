import pygame as py

class Fish:
    def __init__(self, x, y, width, height, imageIn):
        self.fish = py.Rect(x, y, width, height)
        self.image = py.transform.scale(imageIn, (width, height))  # Ensure the image is scaled to the correct size

    def draw(self, surfaceIn):
        surfaceIn.blit(self.image, (self.fish.x, self.fish.y))  # Corrected the blit method to use a tuple for position


    def get(self) -> dict[str, int]:
        return {
            "x": self.fish.x,
            "y": self.fish.y,
            "w": self.fish.width,
            "h": self.fish.height,
        }