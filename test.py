from classes import *
import time
import pygame
pygame.init()

previous_time = time.time()
height, width = 500,500
screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
surface.setAngle(0,90)

particle1 = dust(surface, (15,15))
particle2 = dust(surface, (14,12))
particle3 = dust(surface, (10,10))

while True:

    # #Pygame events iteration
    # for event in pygame.event.get():
    #     if event.type == pygame.quit():
    #         pygame.quit()
    #         break

    #     if event.type == pygame.MOUSEWHEEL:
    #         if pygame.key.get_pressed[pygame.K_LSHIFT]:
    #             surface.addAngle(0,event.y)
    #         else:
    #             surface.addAngle(event.y, 0)

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    screen.fill((0,0,0))
    force = surface.force()
    
    #Particle updates
    for particle in surface.contents:
        particle.updatePos(deltaTime, force)
        particle.draw(screen)

    pygame.display.update()
    surface.positions = []
