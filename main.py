from classes import *
from button import Button
import time
import pygame

pygame.init()
clock = pygame.time.Clock()

previous_time = time.time()
height, width = 700, 700
screen = pygame.display.set_mode((width,height), flags= pygame.RESIZABLE)
surface = plane((width/10,height/10))

clear_button = Button((50,10),(20,50),"clear", (150,150,150), (10,10,10), surface.clear)



pygame.mouse.set_pos((height/2, width/2))




while True:

    clock.tick()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            break


        if event.type == pygame.KEYDOWN:
            surface.clear()

        clear_button.handle_events(event)

    clear_button.draw(screen)

    if pygame.mouse.get_pressed()[0]:
        mX, mY = pygame.mouse.get_pos()
        if dust.gridPos(mX/10, mY/10) not in  surface.positions:
            surface.contents.append(dust(surface, (mX/10, mY/10),mass = random.randint(10, 30)/10))

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    force = surface.force()
    
    #Particle updates
    surface.update(screen, deltaTime , force)

    surface.followMouse(surface)
    surface.indicator(screen)


    pygame.display.set_caption(f"pixel-dust | trimpta | FPS: {clock.get_fps():.0f} | PC: {len(surface.contents)}")
    pygame.display.update()
    screen.fill((0,0,0))

    surface.updateSize(screen)