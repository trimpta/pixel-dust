# /// script
# dependencies = [
#  "plyer",
# ]
# ///

from classes import *
import time
import pygame
import asyncio

try:
    import plyer
    plyer.accelerometer.enable()
    accel = True
except Exception as e:
    accel = False


pygame.init()
clock = pygame.time.Clock()

previous_time = time.time()
height, width = 700,700
screen = pygame.display.set_mode((width,height), flags= pygame.RESIZABLE)
surface = plane((width/10,height/10), screen=screen)

clear_button = Button((50,10),(80,40),"clear", (150,150,150), (5,10,30), surface.clear)



pygame.mouse.set_pos((height/2, width/2))


async def main():

    global accel, previous_time

    while True:

        clock.tick()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                break


            if event.type == pygame.KEYDOWN:
                surface.clear()

            clear_button.handle_events(event)

        if pygame.mouse.get_pressed()[0]:
            mX, mY = pygame.mouse.get_pos()
            surface.contents.append(dust(surface, (mX/10, mY/10),mass = random.randint(10, 30)/10))

        #Loop variables
        deltaTime = time.time() - previous_time
        previous_time = time.time()
        
        if accel:
           force = (-1 * plyer.accelerometer.get_acceleration()[0], plyer.accelerometer.get_acceleration()[1])
        else:
            surface.followMouse()
            force = surface.force()

        clear_button.draw(screen)
        surface.drawGrid()
        surface.indicator()
        
        #Particle updates
        surface.update(deltaTime , force)

        pygame.display.set_caption(f"pixel-dust | trimpta | FPS: {clock.get_fps():.0f} | PC: {len(surface.contents)}")
        pygame.display.update()
        screen.fill((5,1,20))

        surface.updateSize()

        await asyncio.sleep(0)

asyncio.run(main())