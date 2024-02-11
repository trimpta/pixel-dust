from classes import *
import time
import pygame
pygame.init()

previous_time = time.time()
height, width = 600, 600
screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
surface.setAngle(30,30)

particle1 = dust(surface, (0,4))
particle2 = dust(surface, (0,3))

for x in range(1, int(width/10)):
    for y in range(1, int(height/200)):
        surface.contents.append(dust(surface, (x, y)))

while True:


    #Pygame events iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    surface.followMouse(surface)

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    screen.fill((0,0,0))
    force = surface.force()
    
    #Particle updates
    for particle in surface.contents:
        particle.updatePos(deltaTime*2, force)
        particle.draw(screen)
    
    pygame.display.set_caption(f"pixel-dust | Trimpta | FPS: {0 if not deltaTime else 0.1/deltaTime:.0f}")
    surface.indicator(screen)
    pygame.display.update()

    surface.positions = []