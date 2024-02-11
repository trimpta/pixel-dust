from classes import *
import time
import pygame
pygame.init()
clock = pygame.time.Clock()

previous_time = time.time()
height, width = 700,700
screen = pygame.display.set_mode((width,height))

surface = plane((width/10,height/10))
# surface.setAngle(0,0.52359878*2)

# particle2 = dust(surface, (40,40))
# particle1 = dust(surface, (40,30))

for x in range(1, int(width/10)):
    for y in range(1, int(height/200)):
        surface.contents.append(dust(surface, (x, y)))

while True:

    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    surface.followMouse(surface)

    #Loop variables
    deltaTime = time.time() - previous_time
    previous_time = time.time()
    force = surface.force()
    
    #Particle updates
    for particle in surface.contents:
        particle.updatePos(deltaTime, force)
        particle.draw(screen)
    
    pygame.display.set_caption(f"pixel-dust | trimpta | FPS: {clock.get_fps():.0f} | PC: {len(surface.contents)}")
    surface.indicator(screen)
    pygame.display.update()
    screen.fill((0,0,0))

    surface.positions = []