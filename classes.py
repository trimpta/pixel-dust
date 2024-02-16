#17:42 10-02-2024
import math
import pygame
import random
from typing import Tuple, Union

class plane:

    g = 9.8

    def __init__(self, size:tuple[int,int], screen, skewX:int = 0, skewY:int = 0, contents:list = []) -> None:
        
        self.skewX = 0
        self.skewY = 0

        self.forceX = 0
        self.forceY = 0

        self.sizeX, self.sizeY = size[0]/10, size[1]/10
        self.screenW, self.screenH = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = screen

        self.contents = contents
        self.positions = []

    def maxAngle(self):
        self.skewX = 90 if self.skewX > 90 else self.skewX
        self.skewX = -90 if self.skewX < -90 else self.skewX
        self.skewY = 90 if self.skewY > 90 else self.skewY
        self.skewY = -90 if self.skewY < -90 else self.skewY

    def setAngle(self, x, y):
        self.skewX, self.skewY = x, y
        self.maxAngle()
    
    def addAngle(self, x, y):
        self.skewX += x
        self.skewX += y
        self.maxAngle()

    def followMouse(self):
        unitX, unitY = (2*math.pi)/self.screenW, (2*math.pi)/self.screenH
        
        x = pygame.mouse.get_pos()[0] - self.screenW/2
        y = pygame.mouse.get_pos()[1] - self.screenH/2

        self.setAngle(x * unitX, y * unitY)

    def update(self, deltaTime, force):
        for particle in self.contents:
            particle.updatePos(deltaTime, force)
            particle.draw(self.screen)     

    def force(self):
        self.forceX = plane.g * math.sin(self.skewX)
        self.forceY = plane.g * math.sin(self.skewY)

        return (self.forceX, self.forceY)
    
    def indicator(self):
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        unitX, unitY = w/(2*math.pi), h/(2*math.pi)
        center = (round(w/2),round(h/2))
        end_pos = (round( self.skewX * unitX + w/2 ), round( self.skewY * unitY + h/2 ))
        pygame.draw.line(self.screen,(110,100,110), center, (end_pos))

    def drawGrid(self):
        for i in range(0,self.screenW, 10):
            pygame.draw.line(self.screen, (0,10,30), (i,0), (i,self.screenH))

        for i in range(0,self.screenH, 10):
            pygame.draw.line(self.screen, (0,10,30), (0, i), (self.screenW, i))

    def updateSize(self):
        self.sizeX, self.sizeY = pygame.display.Info().current_w/10 , pygame.display.Info().current_h/10

    def clear(self):
        self.contents = []
        dust.id = 0

class dust:

    id = 0
    dampCollisions = 5

    def __init__(self, plane, pos:tuple[int,int], mass:int = 1, color:str = False, vel:tuple[int,int] = (0, 0)) -> None:
        
        self.plane = plane
        self.mass = mass
        self.posX,self.posY = pos
        self.velX, self.velY = vel
        self.mass = mass
        self.id = dust.id
        dust.id +=1

        if color:
            self.color = color
        else:
            self.color = (random.randint(30,255),random.randint(30,255),random.randint(30,255))

        self.plane.contents.append(self)
        self.plane.positions.append(self.pos())

        if not (0<self.posX<self.plane.sizeX or 0<self.posY<self.plane.sizeY):
            raise ValueError('dust must be inside your plane!!!')

    @staticmethod
    def gridPos(x,y):
        return (math.floor(x)*10,math.floor(y)*10)

    def pos(self):
        return (math.floor(self.posX)*10,math.floor(self.posY)*10)
        
    def updatePos(self, deltaTime, force):

        velX = self.velX + force[0]*deltaTime/self.mass * 300
        velY = self.velY + force[1]*deltaTime/self.mass * 300

        x = self.posX + velX * deltaTime * 10
        y = self.posY + velY * deltaTime * 10
        
        if not 0.1<x<self.plane.sizeX-0.1: #i wasted 4 hours here trying to fix collission and all i had to do was use 0.01 instead of 0.1 kms
                x = self.posX
                self.velX *= -1 * dust.dampCollisions
        
        if not 0.01<y<self.plane.sizeY-0.01:
                y = self.posY
                self.velY *= -1 * dust.dampCollisions

        newPos = self.gridPos(x,y)
        for id, pos in enumerate(self.plane.positions):
            if newPos == pos and id != self.id:
            
                x, y = self.posX, self.posY
                self.velX *= -1 * dust.dampCollisions
                self.velY *= -1 * dust.dampCollisions

            # if (dust.gridPos(newPos[0], self.posY)) not in self.plane.positions:
            #     x = self.posX

            # if (dust.gridPos(self.posX , newPos[1] )) not in self.plane.positions:
            #     y = self.posY
                


        self.posX, self.posY = x, y


        self.plane.positions[self.id] = self.pos()
        

    def draw(self,screen):
        x,y = self.pos()
        pygame.draw.rect(screen, self.color,(x,y,10,10),5,2)


class Button:
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        text: str,
        text_color: Union[str, Tuple[int, int, int]],
        bg_color: Union[str, Tuple[int, int, int]],
        method: callable = lambda: None,
    ) -> None:
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.SysFont("Arial", size[1])
        self.text_surf = self.font.render(text, False, text_color)

        self.color = bg_color
        self.text = text
        self.func = method

        self._text_pos = self.text_surf.get_rect(center=self.rect.center).topleft

        self._is_pressed = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the pygame.Rect and font"""
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(
            self.text_surf,
            self._text_pos,
        )

    def handle_events(self, event: pygame.event.Event) -> None:
        """Put this inside of your event loop"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self._is_pressed = True
            else:
                self._is_pressed = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if self._is_pressed and self.rect.collidepoint(event.pos):
                self.func()
            self._is_pressed = False
