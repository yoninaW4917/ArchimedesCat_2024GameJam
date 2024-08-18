import pygame
from player import Player
from objects.block import Block
from objects.fish import Fish
from objects.scale import Scale
from levelEditor.levelEditor import LevelGenerator
import fileLoader

pygame.display.init()

mainSurface = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Fat Cat")

clock = pygame.time.Clock()
level_gen = LevelGenerator()
level: int = 8
cat : Player = Player(level_gen.get(str(level), "starting_pos"),(100,100))
#blocks : list[Block] = [Block((0, 1000), (1920, 80), fileLoader.loadImage("Block.png")), Block((0, 0), (80, 1080), fileLoader.loadImage("Block.png")), Block((800, 0), (80, 1080), fileLoader.loadImage("Block.png"))]
blocks : list[Block] = level_gen.generate_blocks(str(level))
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

    cat.update(keyDown, blocks)

    # ------- DRAWING ------- #
    mainSurface.fill((255, 255, 255))
    background = fileLoader.loadImage(level_gen.get(str(level), "level_background"))
    imageRect = background.get_rect()

    for block in blocks:
        block.draw(mainSurface)

    mainSurface.blit(background, imageRect)

    cat.draw(mainSurface)

    pygame.display.flip()
    clock.tick(60)
