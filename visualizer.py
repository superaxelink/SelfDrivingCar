import numpy as np

import utils as ut
import pygame as pg
class Visualizer():
    
    @staticmethod
    def drawNetwork(surface,network):
      margin = 50
      left = margin
      top = margin
      width, height= surface.get_size()
      width -=2*margin
      height -=2*margin
      levelHeight = height/len(network.levels)
      for i in range(len(network.levels)-1,-1,-1):
        levelTop = top + ut.lerp(height-levelHeight,0, 0.5 if len(network.levels)==1 else i/(len(network.levels)-1))
        Visualizer.drawLevel(surface, network.levels[i], left, levelTop, width, levelHeight)
      #Visualizer.drawLevel(surface, network.levels[0],
      #                     left, top,
      #                     width, height)
    
    @staticmethod
    def drawLevel(surface, level, left, top, width, height):
      right = width + left
      bottom = height+top

      inputs = level.inputs
      outputs = level.outputs
      weights = level.weights
      biases = level.biases
      black = (0,0,0)

      #connections
      for i in range(len(inputs)):
        for j in range(len(outputs)):
          colorConnections = ut.getRGBA(weights[i][j])
          pg.draw.line(
            surface, 
            colorConnections, 
            (Visualizer.getNodeX(inputs, i, left, right), bottom), 
            (Visualizer.getNodeX(outputs, j, left, right), top), 
            2)

      nodeRadius=20
      #down level
      for i in range(len(inputs)):
        x = Visualizer.getNodeX(inputs, i, left, right)
        pg.draw.circle(surface, black, (x, bottom), nodeRadius) 
        pg.draw.circle(surface, ut.getRGBA(inputs[i]), (x, bottom), nodeRadius*0.6) 
      
      #top level
      for i in range(len(outputs)):
        x = Visualizer.getNodeX(outputs, i, left, right)
        pg.draw.circle(surface, black, (x, top), nodeRadius) 
        pg.draw.circle(surface, ut.getRGBA(outputs[i]), (x, top), nodeRadius*0.6) 
        pg.draw.circle(surface, ut.getRGBA(biases[i]), (x, top), nodeRadius*0.8,2)  
    
    @staticmethod
    def getNodeX(nodes, index, left, right):
      return ut.lerp(left, right, 0.5 if len(nodes)==1 else index/(len(nodes)-1))

        


