import numpy as np
import fileLoader
import pygame

def clamp(value, minBound, maxBound):
    return np.clip(value, minBound, maxBound)

def drawcat(surfaceIn):
    cat = fileLoader.loadImage("alive_cat.png").convert()
    current_image = pygame.transform.scale(cat, (cat.get_width()/1.7, cat.get_height()/1.7))
    surfaceIn.blit(current_image, (1450, 640))