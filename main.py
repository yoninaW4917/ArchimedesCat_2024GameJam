import pygame
from player import Player
from objects.block import Block
import fileLoader
from objects.water import Water

pygame.display.init()
pygame.font.init()  # Initialize the font module


mainSurface = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Fat Cat")

clock = pygame.time.Clock()

cat : Player = Player((300, 400))
blocks : list[Block] = [Block((0, 1000), (1920, 80), fileLoader.loadImage("Block.png")), Block((0, 0), (80, 1080), fileLoader.loadImage("Block.png")), Block((400, 0), (80, 300), fileLoader.loadImage("Block.png")), Block((0, 0), (1920, 80), fileLoader.loadImage("Block.png")), Block((400, 400), (80, 800), fileLoader.loadImage("Block.png"))]
waters = [Water(500, 400, 500, 80, fileLoader.loadImage("Water.png"))]  # Ensure the correct image is loaded

running = True

while running:
    # ------- EVENTS ------- #

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            break

        if ev.type == pygame.KEYDOWN:
            # THIS SHOULD BE THE ONLY BUTTON EVENT HANDLING SPEAK TO ALEXANDER IF YOU HAVE QUESTIONS
            if ev.key == pygame.K_ESCAPE:
                running = False
                break

    # ------- UPDATES ------- #

    keyDown = pygame.key.get_pressed()

    cat.update(keyDown, blocks, waters)

    # ------- DRAWING ------- #
    mainSurface.fill((255, 255, 255))

    for block in blocks:
        block.draw(mainSurface)
    
    for water in waters:
        water.draw(mainSurface)  # Ensure the water objects are drawn

    cat.draw(mainSurface)

    pygame.display.flip()
    clock.tick(60)