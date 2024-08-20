from ast import main
import glob
import pygame
from player import Player
from objects.block import Block
from objects.fish import Fish
from objects.scale import Scale
from objects.poof import Poof
from levelEditor.levelEditor import LevelGenerator
import fileLoader
import utils
from utils import Button


pygame.display.init()
pygame.font.init()

mainSurface = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Fat Cat")

clock = pygame.time.Clock()
level_gen = LevelGenerator()
level: int = 1
poof = Poof()
cat : Player = Player(level_gen.get(str(level), "starting_pos"),(100,67), poof)
blocks : list[Block] = level_gen.generate_object(str(level), Block, "blocks")
fishes : list[Fish] = level_gen.generate_object(str(level), Fish, "fish")
scales : list[Scale] = level_gen.generate_object(str(level), Scale, "scales")

buttons : dict[str, Button] = {
    "START" : Button((820, 750), (250, 100), fileLoader.loadImage("UI/PLAY BUTTON.png")),
    "RESUME" : Button((820, 500), (250, 100), fileLoader.loadImage("UI/RESUME BUTTON.png"))
}

gameState = "menu"

running = True

if level in (6, 7):
    addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
    addonRect = addon.get_rect()

def loadNewLevel(level : str) -> pygame.Surface:
    global blocks, fishes, scales, addon, addonRect

    cat.pos = level_gen.get(str(level), "starting_pos").copy()
    cat.startingPos = cat.pos.copy()
    cat.catSize = 100

    if level in ("6", "7"):
        addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
        addonRect = addon.get_rect()

    blocks = level_gen.generate_object(str(level), Block, "blocks")
    fishes = level_gen.generate_object(str(level), Fish, "fish")
    scales = level_gen.generate_object(str(level), Scale, "scales")

    return fileLoader.loadImage(level_gen.get(str(level), "level_background")).convert()

background = loadNewLevel(level)
scales_in_level = cat.get_scale_count_level()
while running:
    # ------- EVENTS ------- #

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            break

        if ev.type == pygame.KEYDOWN:
            # THIS SHOULD BE THE ONLY BUTTON EVENT HANDLING SPEAK TO ALEXANDER IF YOU HAVE QUESTIONS
            if ev.key == pygame.K_ESCAPE:
                if gameState != "game":
                    running = False
                    break
                
                gameState = "pause"

                buttons["RESUME"].draw(mainSurface)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if gameState == "menu":
                    if buttons["START"].withinBounds(pygame.mouse.get_pos()):
                        gameState = "game"

                elif gameState == "pause":
                    if buttons["RESUME"].withinBounds(pygame.mouse.get_pos()):
                        gameState = "game"

    # ------- UPDATES ------- #

    if gameState == "game":
        keyDown = pygame.key.get_pressed()

        if cat.update(keyDown, blocks, scales, fishes):
            # Level complete
            level += 1
            cat.set_scale_count_level(0)
            background = loadNewLevel(str(level))
    elif gameState == "menu":
        pass

    if gameState == "game":
        # ------- DRAWING ------- #
        mainSurface.blit(background, (0, 0))

        cat.draw(mainSurface)

        if (level != 10):
            for fish in fishes:
                fish.draw(mainSurface)

        cat.draw(mainSurface)
        for block in blocks:
            block.draw(mainSurface)
        if (level != 10):
            for fish in fishes:
                fish.draw(mainSurface)
                for scale in scales:
                    scale.draw(mainSurface)

        else:
            utils.drawcat(mainSurface)

        if (level in (6, 7)):
            mainSurface.blit(addon, addonRect)

    elif gameState == "menu":
        mainSurface.blit(background, (0, 0))

        buttons["START"].draw(mainSurface)

    pygame.display.flip()
    clock.tick(60)