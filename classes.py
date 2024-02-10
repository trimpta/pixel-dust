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

    def force(self):
        self.forceX = plane.g * math.sin(self.skewX)
        self.forceY = plane.g * math.sin(self.skewY)

        return (self.forceX, self.forceY)
    
    def indicator(self,screen):
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        unitX, unitY = w/90, h/90
        center = (round(w/2),round(h/2))

        end_pos = (round(self.skewX*unitX+center[0]), round(self.skewY*unitY+center[1]))
        pygame.draw.line(screen,(50,50,100), center, (end_pos))

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
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


        self.plane.contents.append(self)

        if not (0<self.posX<self.plane.sizeX or 0<self.posY<self.plane.sizeY):
            raise ValueError('dust must be inside your plane!!!')
        
    def pos(self):
        return (math.floor(self.posX)*10,math.floor(self.posY)*10)
        
    def updatePos(self, deltaTime, force, bug):

        velX = self.velX + 0.5*force[0]*deltaTime**2/self.mass * 1000
        velY = self.velY + 0.5*force[1]*deltaTime**2/self.mass * 1000

        x = self.posX + velX
        y = self.posY + velY

        if not 0.1<x<self.plane.sizeX-0.1:
                x = self.posX
        
        if not 0.1<y<self.plane.sizeY-0.1:
                y = self.posY

        newPos = (math.floor(x)*10, math.floor(y)*10)
        if bug:
            print('update', self.id, newPos, self.plane.positions)

        for position in self.plane.positions:
            if position[1] == newPos:
                self.plane.positions.append((self.id,self.pos()))
                print('a',self.id,position[0],self.pos())
                return

        self.posX, self.posY = x, y


        self.plane.positions.append((self.id,self.pos()))

    def draw(self,screen):
        x,y = self.pos()
        pygame.draw.rect(screen, self.color,(x,y,10,10))
