import fileLoader
import pygame
import math

class Poof:
    def __init__(self):
        self.frame = 0
        self.val = 0
        self.size = "med"
        self.max_val = 900  # Extended duration for the animation

        # Load poof images for different sizes
        self.images_med = [fileLoader.loadImage(f"mPoof/mPoof-{i}.png") for i in range(5)]
        self.images_lar = [fileLoader.loadImage(f"lPoof/lPoof-{i}.png") for i in range(6)]

        self.isDrawing = False

    def reset(self):
        self.val = 0
        self.frame = 0

    def draw(self, posIn : list[int, int], sizeIn : list[int, int], surfaceIn):
        if self.size == "med":
            self.scale = sizeIn * 2 / 295
            dimensions = (self.scale * 295, self.scale * 216)
        if self.size == "lar":
            self.scale = sizeIn * 2 / 550
            dimensions = (self.scale * 550, self.scale * 363)
        if self.isDrawing:
            # Select the right image set based on size
            if self.size == "med" and self.val < 30:  # Adjusted timing
                current_image = self.images_med[self.frame]
                self.val += 1
                self.frame = math.floor(self.val / 6) % 5  # Slower frame rate
            elif self.size == "lar" and self.val < 40:  # Adjusted timing
                current_image = self.images_lar[self.frame]
                self.val += 1
                self.frame = math.floor(self.val / 7) % 6  # Slower frame rate

            current_image = pygame.transform.scale(current_image, dimensions)
            surfaceIn.blit(current_image, (posIn[0] - 0.5 * sizeIn, posIn[1]-20))  # Adjusted position

            if (self.size == "med" and self.val >= 30) or (self.size == "lar" and self.val >= 40):
                self.reset()
                self.isDrawing = False

