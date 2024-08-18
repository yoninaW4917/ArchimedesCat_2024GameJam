import pygame
from player import Player
from objects.block import Block
import fileLoader
from objects.scale import Scale
from objects.fish import Fish

pygame.display.init()
pygame.font.init()

mainSurface = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Fat Cat")

clock = pygame.time.Clock()

cat : Player = Player((300, 400))
blocks : list[Block] = [Block((0, 1000), (1920, 80), fileLoader.loadImage("Block.png")), Block((0, 0), (80, 1080), fileLoader.loadImage("Block.png")), Block((400, 0), (80, 300), fileLoader.loadImage("Block.png")), Block((0, 0), (1920, 80), fileLoader.loadImage("Block.png")), Block((400, 400), (80, 800), fileLoader.loadImage("Block.png"))]
scales : list[Scale] = [Scale(100, 100, 50, 50, fileLoader.loadImage("Scale.png"))]
fishes : list[Fish] = [Fish(400, 200, 50, 50, fileLoader.loadImage("Fish.png"))]
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

    cat.update(keyDown, blocks, scales, fishes)

    # ------- DRAWING ------- #
    mainSurface.fill((255, 255, 255))

    for block in blocks:
        block.draw(mainSurface)
    for scale in scales:
        scale.draw(mainSurface)
    for fish in fishes:
        fish.draw(mainSurface)

    cat.draw(mainSurface)

    pygame.display.flip()
    clock.tick(60)