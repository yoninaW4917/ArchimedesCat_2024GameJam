import fileLoader
import pygame

CAT_IMAGES = [(fileLoader.loadImage("skinnyCat.png"), (11, 70)), (fileLoader.loadImage("normalCat.png"), (71, 130)), (fileLoader.loadImage("fatCat.png"), (131, 190))]
SLIDER_IMAGE = pygame.transform.scale(fileLoader.loadImage("slider.png"), (40, 120))
CAT_PAW_IMAGE = pygame.transform.scale(fileLoader.loadImage("catPaw.png"), (15, 15))

class Player():
    def __init__(self, startingPos : tuple[int, int] = (0, 0), sizeIn : tuple=(100, 100)) -> None:
        # POS IS THE BOTTOM LEFT CORNER!
        self.pos = [startingPos[0], startingPos[1]]

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

    def update(self, keysDownIn : dict[str, bool]) -> None:
        if keysDownIn[self.keyBinds["scaleUp"]] or keysDownIn[self.keyBinds["scaleDown"]] and self.showSlider == 0:
            self.showSlider = keysDownIn[self.keyBinds["scaleUp"]] - keysDownIn[self.keyBinds["scaleDown"]]

        if self.showSlider != 0:
            self.scaleTimer += self.showSlider * 1.5

            if keysDownIn[self.keyBinds["scaleConfirm"]]:
                self.showSlider = 0
                self.catSize += self.scaleTimer
                self.scaleTimer = 0
            

        self.pos[0] += keysDownIn[self.keyBinds["right"]] - keysDownIn[self.keyBinds["left"]]

        # self.pos[1] += 1
    
    def draw(self, surfaceIn : pygame.Surface) -> None:
        surfaceIn.blit(pygame.transform.scale(self.image, (self.size[0] * self.catSize / 100, self.size[1] * self.catSize / 100)), (self.pos[0], self.pos[1] - self.size[1] * self.catSize / 100))
        
        if self.showSlider != 0:
            surfaceIn.blit(SLIDER_IMAGE, (self.pos[0] + self.size[0] * self.catSize / 100 + 50, self.pos[1] - self.size[1] * self.catSize / 100 * 2))
            surfaceIn.blit(CAT_PAW_IMAGE, (self.pos[0] + self.size[0] * self.catSize / 100 + 50 + SLIDER_IMAGE.get_width() // 2 + CAT_PAW_IMAGE.get_width(), self.pos[1] - self.size[1] * self.catSize / 100 * 2 + SLIDER_IMAGE.get_height() // 2 - CAT_PAW_IMAGE.get_height() // 2 + SLIDER_IMAGE.get_height() * (100 - (self.catSize + self.scaleTimer)) / 100))

        pygame.draw.circle(surfaceIn, (255, 0, 0), (self.pos[0], self.pos[1] + 10), 10)