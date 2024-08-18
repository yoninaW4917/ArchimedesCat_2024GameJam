import pygame as py

class Scale:
    def __init__(self, x, y, width, height, imageIn):
        self.scale = py.Rect(x, y, width, height)
        self.image = py.transform.scale(imageIn, (width, height))  # Ensure the image is scaled to the correct size

    def draw(self, surfaceIn):
        surfaceIn.blit(self.image, (self.scale.x, self.scale.y))  # Corrected the blit method to use a tuple for position


    def get(self) -> dict[str, int]:
        return {
            "x": self.scale.x,
            "y": self.scale.y,
            "w": self.scale.width,
            "h": self.scale.height
        }