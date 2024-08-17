import pygame as py
from objects.block import Block

#setup
py.init()
windowwidth = 1920
windowheight = 1080
window = py.display.set_mode((windowwidth,windowheight))
py.display.set_caption("Catass Level Editor")
clock = py.time.Clock()

#draw loop
while True:
    #check for events
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    
    window.fill("white")

    #draw here
    
    py.display.flip()
    clock.tick(60)
py.quit()