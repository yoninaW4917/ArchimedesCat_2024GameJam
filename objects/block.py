import pygame

class Block():
    def __init__(self, posIn : tuple[int, int], sizeIn : tuple[int, int], imageIn : pygame.image) -> None:
        self.pos = posIn

        self.size = sizeIn

        self.image = pygame.transform.scale(imageIn, self.size)

    def get(self) -> dict[str, int]:
        return {
            "x" : self.pos[0],
            "y" : self.pos[1],
            "w" : self.size[0],
            "h" : self.size[1]
        }

    def draw(self, surfaceIn : pygame.Surface):
        surfaceIn.blit(self.image, self.pos)