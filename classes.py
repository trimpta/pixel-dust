#17:42 10-02-2024
import math
import pygame
import random
class plane:

    g = 9.8

    def __init__(self, size:tuple[int,int], skewX:int = 0, skewY:int = 0, contents:list = []) -> None:
        
        self.skewX = 0
        self.skewY = 0

        self.forceX = 0
        self.forceY = 0

        self.sizeX, self.sizeY = size
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

    def followMouse(self,screen):
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        unitX, unitY = (2*math.pi)/w, (2*math.pi)/w
        
        x = pygame.mouse.get_pos()[0] - w/2
        y = pygame.mouse.get_pos()[1] - h/2

        self.setAngle(x * unitX, y * unitY)
        

    def force(self):
        self.forceX = plane.g * math.sin(self.skewX)
        self.forceY = plane.g * math.sin(self.skewY)

        return (self.forceX, self.forceY)
    
    def indicator(self,screen):
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        unitX, unitY = w/(2*math.pi), h/(2*math.pi)
        center = (round(w/2),round(h/2))
        end_pos = (round( self.skewX * unitX + w/2 ), round( self.skewY * unitY + h/2 ))
        pygame.draw.line(screen,(110,100,110), center, (end_pos))

class dust:

    id = 0

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

        if not (0<self.posX<self.plane.sizeX or 0<self.posY<self.plane.sizeY):
            raise ValueError('dust must be inside your plane!!!')

    @staticmethod
    def gridPos(x,y):
        return (math.floor(x)*10,math.floor(y)*10)

    def pos(self):
        return (math.floor(self.posX)*10,math.floor(self.posY)*10)
        
    def updatePos(self, deltaTime, force):

        velX = self.velX + force[0]*deltaTime/self.mass * 1000
        velY = self.velY + force[1]*deltaTime/self.mass * 1000

        x = self.posX + velX * deltaTime
        y = self.posY + velY * deltaTime

        if not 0.1<x<self.plane.sizeX-0.1: #i wasted 4 hours here trying to fix collission and all i had to do was use 0.01 instead of 0.1 kms
                x = self.posX
        
        if not 0.01<y<self.plane.sizeY-0.01:
                y = self.posY

        newPos = self.gridPos(x,y)
        if newPos in self.plane.positions:

            if (dust.gridPos(newPos[0], self.posY)) in self.plane.positions:
                y = self.posY

            if (dust.gridPos(self.posX , newPos[1] )) in self.plane.positions:
                x = self.posX


        self.posX, self.posY = x, y


        self.plane.positions.append(self.pos())

    def draw(self,screen):
        x,y = self.pos()
        pygame.draw.rect(screen, self.color,(x,y,10,10))
