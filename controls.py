import pygame as pg

class Controls():
  
  def __init__(self, type):
    #self.game = game


    self.key_mapping = {
      pg.K_LEFT: "left",
      pg.K_RIGHT: "right",
      pg.K_UP: "forward",
      pg.K_DOWN: "reverse"
    }

    self.forward = False
    self.left = False
    self.right = False
    self.reverse = False

    self.gameOn = True
    self.type=type

  def control(self, eventList):
    if(self.type=="KEYS" or self.type=="AI"):
      return self.addKeyBoardListeners(eventList)
    elif(self.type =="DUMMY"):
      self.forward=True

  
  def addKeyBoardListeners(self,eventList):
    if(self.type=="KEYS"):
      for event in eventList:
        if event.type == pg.KEYDOWN or event.type==pg.KEYUP:
            key = event.key
            action = self.key_mapping.get(key)
            if action is not None:
              setattr(self, action, event.type == pg.KEYDOWN)
        if event.type == pg.QUIT:
          self.gameOn = False
    
    if(self.type=="AI"):
      for event in eventList:
        if event.type == pg.QUIT:
          self.gameOn = False
    
