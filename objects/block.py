import pygame

class Block():
    def __init__(self, posIn : list[int, int], sizeIn : list[int, int], imageIn : pygame.image, water = False) -> None:
        self.pos = posIn

        self.size = sizeIn

        self.image = pygame.transform.scale(imageIn, self.size)

        self.water = water

    def get(self) -> dict[str, int]:
        return {
            "x" : self.pos[0],
            "y" : self.pos[1],
            "w" : self.size[0],
            "h" : self.size[1],
            "water" : self.water
        }

    def draw(self, surfaceIn : pygame.Surface):
        surfaceIn.blit(self.image, self.pos)
