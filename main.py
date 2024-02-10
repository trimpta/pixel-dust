from classes import *
import time
import pygame
pygame.init()

previous_time = time.time()
height, width = 500,500
screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
surface.setAngle(30,10)

particle1 = dust(surface, (0,4))
particle2 = dust(surface, (0,3))
# particle3 = dust(surface, (10,10))

bug = False
while True:


    #Pygame events iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                surface.addAngle(0,event.y)
            else:
                surface.addAngle(event.y, 0)

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    screen.fill((0,0,0))
    force = surface.force()
    
    #Particle updates
    for particle in surface.contents:
        particle.updatePos(deltaTime, force, bug)
        particle.draw(screen)

    surface.indicator(screen)
    pygame.display.update()

    #debugging
    if surface.positions == [(0, (0, 10)), (1, (0, 0))] and not bug:
        bug = True

    if bug:
        # print(particle1.posX, particle1.posY)
        pass

    if surface.positions == [(0, (0, 0)), (1, (0, 0))]:
        break


    surface.positions = []

while True:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        break