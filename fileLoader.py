import os
import pygame
import numpy as np

# https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe

def getPath(localPath : str) -> str:
    base_path = os.path.abspath(".")

    return os.path.join(base_path, localPath)

def loadImage(localImagePath : str) -> pygame.Surface:
    """
    Tries to load an image\n
    Args:
        localImagePath (str): The image path

    Returns:
        pygame.Surface: The loaded image unless the image was not on the path in which case returns a null image
    """
    try:
        return pygame.image.load(f"assets/images/{localImagePath}")
    except FileNotFoundError:
        surface = pygame.Surface((2, 2))
        
        pygame.draw.rect(surface, pygame.Color(247, 2, 215), [0, 0, 1, 1])
        pygame.draw.rect(surface, pygame.Color(247, 2, 215), [1, 1, 1, 1])
        
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), [0, 1, 1, 1])
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), [1, 0, 1, 1])
        
        return pygame.transform.scale(surface, (1024, 1024))
    
def loadFont(localFontPath : str, sizeIn : int) -> pygame.font.Font:
    """
    Tries to load a font
    Args:
        localFontPath (str): The font path
        sizeIn (int): The size of the font

    Returns:
        pygame.font.Font: Returns the loaded font unless the font doesn't exist in which case returns a default font
    """
    try:
        return pygame.font.Font(f"assets/fonts/{localFontPath}", sizeIn)
    except FileNotFoundError:
        return pygame.font.Font(pygame.font.get_default_font(), sizeIn)
    
def loadSound(localSoundPath : str) -> pygame.mixer.Sound:
    """
    Tries to load a sound
    Args:
        localSoundPath (str): The path of the sound

    Returns:
        pygame.mixer.Sound: Returns the loaded sound unless the sound doesn't exist in which case returns an empty sound object
    """
    try:
        return pygame.mixer.Sound(f"assets/sounds/{localSoundPath}")
    except FileNotFoundError:
        # Empty sound file
        return pygame.mixer.Sound(np.zeros((1, 1), dtype=np.int16))
    
if __name__ == '__main__':
    pygame.init()
    
    loadImage("notAImage.png")
    loadFont("notAFont.ttf")
    loadSound("notASound.mp3")
