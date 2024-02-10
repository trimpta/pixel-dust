#17:42 10-02-2024
import math
import pygame

class plane:

    g = 1

    def __init__(self, skewX:int = 0, skewY:int = 0, size:tuple[int,int] = (10,10), contents:list = []) -> None:
        
        self.skewX = 0
        self.skewY = 0

        self.forceX = 0
        self.forceY = 0

        self.sizeX, self.sizeY = size
        self.plane = contents

    def setAngle(self, x, y):
        self.skewX, self.skewY = x, y
    
    def addAngle(self, x, y):
        self.skewX += x
        self.skewX += y

    def force(self):
        self.forceX = plane.g * math.sin(self.skewX)
        self.forceY = plane.g * math.sin(self.skewY)


class dust:

    def __init__(self, plane, pos:tuple[int,int], mass:int = 1) -> None:
        
        self.plane = plane
        self.mass = mass
        self.posX,self.posY = pos
        self.mass = mass

        self.plane.append(self)

        if not (0<self.posX<self.plane.sizeX or 0<self.posY<self.plane.sizeY):
            raise ValueError('dust must be inside your plane!!!')
        
    def updatePos(self, deltaTime, force):

        self.posX += 0.5*force[0]*deltaTime**2
        self.posY += 0.5*force[1]*deltaTime**2

    def draw(self,screen):
