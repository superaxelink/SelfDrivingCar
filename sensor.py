import numpy as np
import pygame as pg
import utils as ut
#from car import Car
#This sensor implements raycasting for detecting roadBorders
class Sensor():
  def __init__(self, car):
    self.car = car
    self.rayCount = 5
    self.rayLength = 150
    self.raySpread = np.pi/2
        
    self.rays = []
    self.readings = []

  def update(self,roadBorders, traffic):
    self.castRays()
    self.readings = []
    for i in range(0, len(self.rays)):
      self.readings.append(
        self.getReading(
        self.rays[i], 
        roadBorders,
        traffic)
      )
  
  def getReading(self, ray, roadBorders, traffic):
    touches = []

    for i in range(0, len(roadBorders)):
      touch = ut.getIntersection(ray[0], ray[1], roadBorders[i][0], roadBorders[i][1])
      if(touch):
        touches.append(touch)

    for i in range(0, len(traffic)):
      poly  = traffic[i].polygon
      for j in range(0, len(poly)):
        value = ut.getIntersection(
          ray[0], 
          ray[1], 
          poly[j], 
          poly[(j+1)%len(poly)])
        if(value):
          touches.append(value)
    
    if(len(touches)==0):
      return None
    else:
      offsets = [e["offset"] for e in touches]
      minOffset = np.min(offsets) #parece que puedo usar tambien solo min() pues es una funcion de python
      foundElement = next((e for e in touches if e['offset'] == minOffset))#,) #next returns the first element that meets the condition
      return foundElement

  def castRays(self):
    self.rays = []
    for i in range(0, self.rayCount):
      rayAngle = ut.lerp(self.raySpread/2, 
                         -self.raySpread/2, 
                         0.5 if self.rayCount==1 else i/(self.rayCount-1)) -self.car.angle
      start = {"x":self.car.x, "y":self.car.y}
      end = {"x":self.car.x + np.sin(rayAngle)*self.rayLength, 
             "y":self.car.y - np.cos(rayAngle)*self.rayLength}
      self.rays.append([start, end])

  def draw(self, screen, x, y, y1):
    for i in range(0, self.rayCount):
      end = self.rays[i][1]
      if(self.readings[i]):
        end = self.readings[i]
      pg.draw.line(screen, (255,255, 0), #yellow
                   (self.rays[i][0]["x"], self.rays[i][0]["y"]),
                   (end["x"], end["y"]),
                   #(self.rays[i][1]["x"], self.rays[i][1]["y"]),
                   2)
      pg.draw.line(screen, (0,0, 0), #black
                   (self.rays[i][1]["x"], self.rays[i][1]["y"]),
                   (end["x"], end["y"]),
                   2)

    



