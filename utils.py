import numpy as np
import fileLoader
import pygame


def clamp(value, minBound, maxBound):
    return np.clip(value, minBound, maxBound)


def drawcat(surfaceIn: pygame.Surface):
    cat = fileLoader.loadImage("alive_cat.png").convert_alpha()
    current_image = pygame.transform.scale(cat, (cat.get_width() / 1.7, cat.get_height() / 1.7))
    surfaceIn.blit(current_image, (1450, 640))


class Button():
    def __init__(self, posIn: tuple[int, int], sizeIn: tuple[int, int], imageIn: pygame.Surface) -> None:
        """
        Creates a new button object
        Args:
            posIn (tuple[int, int]): The screen position of the button
            sizeIn (tuple[int, int]): The size of the button
        """
        self.pos = posIn
        self.size = sizeIn

        self.image = pygame.transform.scale(imageIn, self.size).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def withinBounds(self, mousePos: tuple[int, int]) -> bool:
        """
        If the given mouse pos is within the button
        Args:
            mousePos (tuple[int, int]): the position of the mouse

        Returns:
            bool: True if touching
        """
        return self.rect.collidepoint(mousePos[0], mousePos[1])

    def draw(self, surfaceIn: pygame.Surface) -> None:
        """
        Draw the button on the given surface
        Args:
            surfaceIn (pygame.Surface): The surface to draw the button on
        """
        surfaceIn.blit(self.image, self.pos)