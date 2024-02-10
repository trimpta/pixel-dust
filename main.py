from classes import *
import pygame
pygame.init()


height, width = 500,500
screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
surface.setAngle(-10,-25)

particle = dust(surface, (15,15))

while True:
    screen.fill((0,0,0))
    force = surface.force()
    particle.updatePos(0.1, force)
    particle.draw(screen)
    print(particle.posX,particle.posY)
    pygame.display.update()