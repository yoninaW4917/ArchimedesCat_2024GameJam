import glob
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
level: int = 6
cat : Player = Player(level_gen.get(str(level), "starting_pos"),(100,100))
blocks : list[Block] = level_gen.generate_object(str(level), Block, "blocks")
fishes : list[Fish] = level_gen.generate_object(str(level), Fish, "fish")
scales : list[Scale] = level_gen.generate_object(str(level), Scale, "scales")

running = True

if level in (6, 7):
    addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
    addonRect = addon.get_rect()

def loadNewLevel(level : str) -> pygame.image:
    global blocks, fishes, scales, addon, addonRect

    cat.pos = level_gen.get(str(level), "starting_pos").copy()
    cat.catSize = 100

    if level in ("6", "7"):
        addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
        addonRect = addon.get_rect()

    blocks = level_gen.generate_object(str(level), Block, "blocks")
    fishes = level_gen.generate_object(str(level), Fish, "fish")
    scales = level_gen.generate_object(str(level), Scale, "scales")

    return fileLoader.loadImage(level_gen.get(str(level), "level_background")).convert()

background = loadNewLevel(level)

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

    if cat.update(keyDown, blocks, scales, fishes):
        # Level complete
        level += 1

        background = loadNewLevel(str(level))

    # ------- DRAWING ------- #
    mainSurface.fill((0, 0, 0))

    # for block in blocks:
    #     block.draw(mainSurface)

    mainSurface.blit(background, (0, 0))

    cat.draw(mainSurface)

    if (level != 10):
        for fish in fishes:
            fish.draw(mainSurface)

        for scale in scales:
            scale.draw(mainSurface)

    if (level in (6, 7)):
        mainSurface.blit(addon, addonRect)

    pygame.display.flip()
    clock.tick(60)