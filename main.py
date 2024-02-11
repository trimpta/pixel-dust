from classes import *
import time
import pygame
import asyncio
import plyer



try:
    plyer.accelerometer.enable()
    if plyer.accelerometer.acceleration[0] is None:
        accel = False
        raise ValueError

    accel = True
except Exception as e:
    accel = False

pygame.init()
clock = pygame.time.Clock()

previous_time = time.time()
height, width = 700,700
screen = pygame.display.set_mode((width,height), flags= pygame.RESIZABLE)
surface = plane((width/10,height/10))


async def main():
    global previous_time, accel
    while True:

        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                surface.contents = []

        if pygame.mouse.get_pressed()[0]:
            mX, mY = pygame.mouse.get_pos()
            surface.contents.append(dust(surface, (mX/10, mY/10)))

        if accel:
            surface.setAngle(plyer.accelerometer.acceleration[:-1])
        else:
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
        surface.updateSize(screen)
        pygame.display.update()
        screen.fill((0,0,0))

        surface.positions = []

        await asyncio.sleep(0)

asyncio.run(main())