import fileLoader
import pygame
from objects.block import Block
import utils

CAT_IMAGES = [(fileLoader.loadImage("skinnyCat.png"), (11, 70)), (fileLoader.loadImage("normalCat.png"), (71, 130)), (fileLoader.loadImage("fatCat.png"), (131, 190))]
SLIDER_IMAGE = pygame.transform.scale(fileLoader.loadImage("slider.png"), (40, 120))
CAT_PAW_IMAGE = pygame.transform.scale(fileLoader.loadImage("catPaw.png"), (15, 15))

class Player():
    def __init__(self, startingPos : list[int, int] = (0, 0), sizeIn : tuple=(100, 100)) -> None:
        # POS IS THE BOTTOM LEFT CORNER!
        self.pos = [startingPos[0], startingPos[1]]
        self.velo = [0, 0]

        # This is the image size
        self.size = [sizeIn[0], sizeIn[1]]

        # This is the slider value
        self.catSize = 100

        self.scaleTimer = 0

        self.image = CAT_IMAGES[1][0]

        # 0 for no, 1 for down, -1 for up
        self.showSlider = 0

        self.keyBinds : dict[str, int] = {
            "right" : pygame.K_d,
            "left" : pygame.K_a,
            "jump" : pygame.K_w,
            "scaleUp" : pygame.K_UP,
            "scaleDown" : pygame.K_DOWN,
            "scaleConfirm" : pygame.K_SPACE
        }

    def update(self, keysDownIn : dict[str, bool], blocks : list[Block]) -> None:
        if (keysDownIn[self.keyBinds["scaleUp"]] or keysDownIn[self.keyBinds["scaleDown"]]) and self.showSlider == 0:
            self.showSlider = keysDownIn[self.keyBinds["scaleUp"]] - keysDownIn[self.keyBinds["scaleDown"]]

        if self.showSlider != 0:
            self.scaleTimer += self.showSlider * 1.5

            if keysDownIn[self.keyBinds["scaleConfirm"]]:
                self.showSlider = 0
                self.catSize = 100 + self.scaleTimer / 60 * 100
                self.scaleTimer = 0
                print(self.catSize)

        self.velo[0] = keysDownIn[self.keyBinds["right"]] - keysDownIn[self.keyBinds["left"]]
        self.velo[1] += 0.1

        for block in blocks:
            blockData = block.get()

            self.pos[1] += self.velo[1]

            width = self.size[0] + self.catSize / 100
            height = self.size[1] + self.catSize / 100

            yUndo = False

            # Check for collision on the X and Y axes
            if (self.pos[0] + width > blockData['x'] and
                self.pos[0] < blockData['x'] + blockData['w'] and
                self.pos[1] < blockData['y'] and
                self.pos[1] + height > blockData['y'] + blockData['h']):
 
                # Collision detected, resolve it
                self.pos[1] -= self.velo[1]  # Undo the Y movement
                self.velo[1] = 0             # Stop the Y velocity
                yUndo = True

            if not yUndo:
                self.pos[1] -= self.velo[1]

        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]
    
    def draw(self, surfaceIn : pygame.Surface) -> None:
        surfaceIn.blit(pygame.transform.scale(self.image, (self.size[0] * self.catSize / 100, self.size[1] * self.catSize / 100)), (self.pos[0], self.pos[1] - self.size[1] * self.catSize / 100))
        
        if self.showSlider != 0:
            surfaceIn.blit(SLIDER_IMAGE, (self.pos[0] + self.size[0] * self.catSize / 100 + 50, utils.clamp(self.pos[1] - self.size[1] * self.catSize / 100 * 2, -1000, 850)))
            surfaceIn.blit(CAT_PAW_IMAGE, (self.pos[0] + self.size[0] * self.catSize / 100 + 50 + SLIDER_IMAGE.get_width() // 2 + CAT_PAW_IMAGE.get_width(), utils.clamp(self.pos[1] - self.size[1] * self.catSize / 100 * 2, -1000, 850) + SLIDER_IMAGE.get_height() // 2 - CAT_PAW_IMAGE.get_height() // 2 + SLIDER_IMAGE.get_height() * -self.scaleTimer / 80))


        pygame.draw.circle(surfaceIn, (255, 0, 0), (self.pos[0], self.pos[1] + 10), 10)