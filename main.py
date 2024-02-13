from classes import *
import time
import pygame

pygame.init()
clock = pygame.time.Clock()

previous_time = time.time()
height, width = 700, 700
screen = pygame.display.set_mode((width,height), flags= pygame.RESIZABLE)
surface = plane((width/10,height/10))



pygame.mouse.set_pos((height/2, width/2))




while True:

    clock.tick()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            break


        if event.type == pygame.KEYDOWN:
            surface.clear()

    if pygame.mouse.get_pressed()[0]:
        mX, mY = pygame.mouse.get_pos()
        if dust.gridPos(mX/10, mY/10) not in  surface.positions:
            surface.contents.append(dust(surface, (mX/10, mY/10)))

    surface.followMouse(surface)
    surface.indicator(screen)

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    force = surface.force()
    
    #Particle updates
    surface.update(screen, deltaTime , force)


    pygame.display.set_caption(f"pixel-dust | trimpta | FPS: {clock.get_fps():.0f} | PC: {len(surface.contents)}")
    pygame.display.update()
    screen.fill((0,0,0))

    surface.updateSize(screen)