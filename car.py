import pygame as pg
import numpy as np
import utils as ut
from controls import Controls
from sensor import Sensor
from network import NeuralNetwork

class Car():
  def __init__(self, x, y, width, height, controlType, maxSpeed=3):
    self.x = x
    self.y = y
    self.centralPosition = y
    self.width = width
    self.height = height

    self.infinity = 10000    

    self.speed = 0 
    self.acceleration = 0.002
    self.maxSpeed = maxSpeed
    self.friction =0.001
    self.angle = 0 #in radians
    self.damaged = False

    self.xspeed = 0

    self.updateY=0

    self.useBrain = controlType=="AI"

    self.controlType = controlType

    self.mainCar = False

    self.sensor = None
    self.brain = None

    self.quietCounter = 0

    self.imagePath = "car.png"
    self.image = pg.transform.scale(pg.image.load(self.imagePath).convert_alpha(),(self.width, self.height))

    if(self.controlType!="DUMMY"):
      self.sensor = Sensor(self)
      self.brain = NeuralNetwork([self.sensor.rayCount,6, 4])
    self.controls = Controls(self.controlType)
  
  def draw(self, screen, color):
    if(self.damaged):
      color = (80,80,80)
    #Here we use polygonList for drawing instead of polygon because pg.draw.polygon didn't accept dicts
    if self.sensor is not None and self.mainCar:
      self.sensor.draw(screen, self.x, self.y,500)
    pg.draw.polygon(screen, color, self.polygonList)

    #This is only for styling and better to use it with few cars, slows down everything if you're training
    #rotatedImage= pg.transform.rotate(self.image,np.rad2deg(self.angle)) 
    #mask =pg.mask.from_surface(rotatedImage)
    #maskSurface = mask.to_surface().convert_alpha()
    #maskSurface.set_colorkey((0,0,0))
    #surf_w,surf_h = maskSurface.get_size()
    #for x in range(surf_w):
    #  for y in range(surf_h):
    #    if maskSurface.get_at((x,y))[0]!=0:
    #      maskSurface.set_at((x,y), color) 
    #self.imageRect = maskSurface.get_rect(center=(self.x,self.y))
    #self.imageRect = rotatedImage.get_rect(center=(self.x,self.y))
    #screen.blit(maskSurface,self.imageRect)

    #Here we do it with squares
    #cuadro = pg.Surface((self.width, self.height), pg.SRCALPHA)
    ##cuadro.fill((0, 0, 255))  # Rellena el cuadro con color azul
    #cuadro.fill((0, 0, 0))  # Rellena el cuadro con color negro

    # Rota el cuadro
    ##rotate takes angles in degrees
    #cuadro_rotado = pg.transform.rotate(cuadro, np.rad2deg(self.angle))
    #cuadro_rotado_rect = cuadro_rotado.get_rect(center=(self.x, self.centralPosition))
    ##cuadro_rotado_rect = cuadro_rotado.get_rect(center=(self.x, self.y))

    # Dibuja el cuadro rotado en la pantalla
    #screen.blit(cuadro_rotado, cuadro_rotado_rect.topleft)

    #self.sensor.draw(screen, self.x, self.y,500)
    #screen.blit(cuadro_rotado, (self.x,self.y))

  #def update(self, roadBorders, traffic):
  def update(self, roadBorders, traffic, eventList, spd=0):
    self.controls.control(eventList)
    self.move(spd)
    self.polygon = self.createPolygon()
    self.polygonList = [(point["x"], point["y"]) for point in self.polygon]
    if not self.damaged:
      self.damaged = self.assessDamage(roadBorders, traffic)
    if self.sensor is not None:
      self.sensor.update(roadBorders, traffic)
      #low values if far away higher if closer
      offsets = [0 if s is None else 1 - s["offset"] for s in self.sensor.readings] 
      #HERE WE GIVE INPUTS(OFFSETS) TO THE NEURAL NETWORK
      #get sensor readings(the offsets), this will work as the inputs
      outputs = NeuralNetwork.feedForward(offsets, self.brain)
      #the outputs will be the result from the processed inputs
      if(self.useBrain): 
        #connect brain(outputs) with controls
        self.controls.forward = outputs[0]
        self.controls.left = outputs[1]
        self.controls.right = outputs[2]
        self.controls.reverse = outputs[3]   
    return self.controls.gameOn

  def assessDamage(self,roadBorders, traffic):
    for i in range(0, len(roadBorders)):
      if(ut.polysIntersect(self.polygon, roadBorders[i])):
        return True
    for i in range(0, len(traffic)):
      if(ut.polysIntersect(self.polygon, traffic[i].polygon)):
        return True
    return False

#Here we create an array to contain 4 points which represent the edges of a polygon
  def createPolygon(self):
    points = []
    rad = np.hypot(self.width, self.height)/2
    alpha = np.arctan2(self.width, self.height)
    points.append({
      "x":self.x-np.sin(self.angle-alpha)*rad,#top right
      "y":self.y-np.cos(self.angle-alpha)*rad
    })
    points.append({
      "x":self.x-np.sin(self.angle+alpha)*rad,#top left
      "y":self.y-np.cos(self.angle+alpha)*rad
    })
    points.append({
      "x":self.x-np.sin(np.pi + self.angle-alpha)*rad,#bottom right
      "y":self.y-np.cos(np.pi + self.angle-alpha)*rad
    })
    points.append({
      "x":self.x-np.sin(np.pi + self.angle+alpha)*rad,#bottom left
      "y":self.y-np.cos(np.pi + self.angle+alpha)*rad
    })
    return points

  def move(self,spd):
    self.input()
    #sine and cosine take angles in radians
    self.x -= np.sin(self.angle)*self.speed
    if(self.controlType=="KEYS"):
      self.updateY = np.cos(self.angle)*self.speed 
    if(self.controlType=="AI"):
      if(self.mainCar):
        self.updateY = np.cos(self.angle)*self.speed 
      else:
        self.y -= np.cos(self.angle)*self.speed - spd
    if(self.controlType=="DUMMY"):
      #self.offset = 0-self.y
      #if(self.y<-self.infinity*0.9 or self.y>self.infinity*0.9):
        #self.y-=self.offset
      self.y -= np.cos(self.angle)*self.speed - spd
  
  def input(self):
    if self.damaged:
      self.speed=0
      return 
    if(self.controls.forward):
      self.speed += self.acceleration
    if(self.controls.reverse):
      self.speed -= self.acceleration
    if(self.speed>self.maxSpeed/2):
      self.speed = self.maxSpeed/2
    if(self.speed<-self.maxSpeed):
      self.speed = -self.maxSpeed
    if(self.speed>0):
      self.speed -= self.friction
    if(self.speed<0):
      self.speed += self.friction
    if(np.abs(self.speed)<self.friction):
      self.speed=0
    if(self.speed!=0):
      flip = 1 if self.speed>0 else -1 
      if(self.controls.left):
        self.angle+=0.005*flip
      if(self.controls.right):
        self.angle-=0.005*flip