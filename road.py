import numpy as np
import pygame as pg
import utils as ut


class Road():
  def __init__(self, x, y, width, height, laneCount=3):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.laneCount = laneCount
    self.thickness = 2 

    self.left = x
    self.right =x+width

    self.infinity = 1000    
    self.top = self.infinity #check if computer grows downwards otherwise top=infinity and bottom=-infinity
    self.bottom = -self.infinity
    self.white = (255,255,255)
    self.lightGrey = (128,128,128)
    self.offset = 0

    self.topLeft = {"x":self.left, "y":self.top}
    self.topRight = {"x":self.right, "y":self.top}
    self.bottomLeft = {"x":self.left, "y":self.bottom}
    self.bottomRight = {"x":self.right, "y":self.bottom}

    self.borders = [[self.topLeft, self.bottomLeft],
                    [self.topRight, self.bottomRight]]    

  def update(self,spd):
    self.y+=spd
    self.offset = 0-self.y
    if(self.y<-self.infinity*0.9 or self.y>self.infinity*0.9):
      self.y+=self.offset

  def draw(self, screen):
    #maybe rect shoudl go from bottom to top or something
    #offseta = 0 - self.y
    #print(self.y)
    pg.draw.rect(screen, self.lightGrey, pg.Rect(self.x, self.y-self.infinity, self.width, self.y+3*self.infinity))
    for i in range(0, self.laneCount+1):
      x = ut.lerp(self.x, self.right, i/self.laneCount)
      if(i>0 and i<self.laneCount):
        #self.draw_dashed_line(screen, self.white, (x, self.y+self.height+offset),(x, self.y+offset),self.thickness,20, 20)
        self.draw_dashed_line(screen, self.white, (x, self.y-self.infinity),(x, self.y+self.infinity),self.thickness,20, 20)
        #pg.draw.line(screen, self.white, (x, self.y-self.infinity),(x, self.y+self.infinity),self.thickness)
      else:
        #pg.draw.line(screen, self.white, (x, self.bottom),(x, self.top),self.thickness)
        pg.draw.line(screen, self.white, (x, self.y-self.infinity),(x, self.y+self.infinity),self.thickness)
      

  def getLaneCenter(self,laneIndex):
    laneWidth = self.width/self.laneCount
    return self.x + laneWidth/2 + min(laneIndex, self.laneCount-1)*laneWidth

  def draw_dashed_line(self, screen, color, start, end, thickness, dash_length, gap_length):
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]
    line_length = (delta_x ** 2 + delta_y ** 2) ** 0.5

    step_x = delta_x / line_length
    step_y = delta_y / line_length

    current_x, current_y = start
    #drawing = True

    for distance in range(0, int(line_length), dash_length + gap_length):
        seg_start = (int(current_x), int(current_y))
        current_x += step_x * dash_length
        current_y += step_y * dash_length
        seg_end = (int(current_x), int(current_y))

        pg.draw.line(screen, color, seg_start, seg_end, thickness)

        current_x += step_x * gap_length
        current_y += step_y * gap_length
