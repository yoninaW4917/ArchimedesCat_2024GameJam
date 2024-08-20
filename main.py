from ast import main
import glob
from flask import g
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


pygame.mixer.init()
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

music : dict[str, pygame.mixer.Sound] = {
    "HAPPY" : fileLoader.loadSound("music/Happy cat.mp3"),
    "SAD" : fileLoader.loadSound("music/Sad cat.mp3")
}

gameState = "menu"

running = True

# if level in (6, 7):
#     addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
#     addonRect = addon.get_rect()
def loadCutscenes(scene_no: str):
    pygame.draw.rect(mainSurface, (0, 0, 0), (0, 0, 1920, 1080))
    mainSurface.blit(fileLoader.loadImage(f'Cutscenes/{scene_no}.png').convert(), (210, 40))
    pygame.display.flip()
    pygame.time.wait(5000)
    cat.timer = cat.timer + 5000

def loadNewLevel(level : str) -> pygame.Surface:
    global blocks, fishes, scales, addon, addonRect

    cat.pos = level_gen.get(str(level), "starting_pos").copy()
    cat.startingPos = cat.pos.copy()
    cat.catSize = 100

    if int(level) == 1:
        # Happy
        pygame.mixer.stop()

        music["HAPPY"].play(-1)
    elif int(level) == 5:
        # Sad
        pygame.mixer.stop()

        music["SAD"].play(-1)

    if level in ("6", "7"):
        addon = fileLoader.loadImage(level_gen.get(str(level), "addon")).convert_alpha()
        addonRect = addon.get_rect()

    blocks = level_gen.generate_object(str(level), Block, "blocks")
    fishes = level_gen.generate_object(str(level), Fish, "fish")
    scales = level_gen.generate_object(str(level), Scale, "scales")

    return fileLoader.loadImage(level_gen.get(str(level), "level_background")).convert()

background = loadNewLevel(level)
menu_background = fileLoader.loadImage("./UI/MENU_BG.png")
resume_background = fileLoader.loadImage("./UI/bg_gradient.png")
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
                mainSurface.blit(resume_background, (0, 0))
                buttons["RESUME"].draw(mainSurface)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if gameState == "menu":
                    if buttons["START"].withinBounds(pygame.mouse.get_pos()):
                        for scene_no in range(1,3): loadCutscenes(scene_no)
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
            if level == 5:
                loadCutscenes(3)
            if level >10:
                gameState = "end"
                level = 1
            background = loadNewLevel(str(level))

    if gameState == "game":
        # ------- DRAWING ------- #
        mainSurface.blit(background, (0, 0))

        cat.draw(mainSurface)

        if (level != 10):
            for fish in fishes:
                fish.draw(mainSurface)

        cat.draw(mainSurface)
#        for block in blocks:
#            block.draw(mainSurface)
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
        mainSurface.blit(fileLoader.loadImage('UI/Start.png'), (0, 0))

        buttons["START"].draw(mainSurface)

    elif gameState == 'end':
        # cutscenes here
        for scene_no in range(4,7): loadCutscenes(scene_no)
        gameState = 'menu'

    pygame.display.flip()
    clock.tick(60)