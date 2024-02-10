from classes import *
import pygame
# pygame.init()


height, width = 300,300
# screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
surface.setAngle(30,0)
force = surface.force()

particle = dust(surface, (15,15))


particle.updatePos(5, force)

print(particle.posX,particle.posY)