import json
import os
import copy
import numpy as np
import pygame as pg
from pygame.locals import*
import time as tm
from car import Car
from road import Road
from visualizer import Visualizer
from network import NeuralNetwork


windowWidth = 500
windowWidthTotal = 2*windowWidth
windowHeight = 600
# Inicializar Pygame
pg.init()
screen = pg.display.set_mode((windowWidthTotal, windowHeight))
pg.display.set_caption("Self Driving Car")
#screen = pg.display.set_mode((windowWidth, windowHeight))
left_surface = pg.Surface((windowWidth, windowHeight), pg.SRCALPHA)
right_surface = pg.Surface((windowWidth, windowHeight), pg.SRCALPHA)

pg.event.set_allowed([QUIT, KEYDOWN, KEYUP])

#Colors
backgroundGrey = (102, 102, 102)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

left_surface.fill(backgroundGrey)
right_surface.fill(black)
#screen.fill(backgroundGrey)
right_surface.convert_alpha()
left_surface.convert_alpha()
road = Road(150, 0, 200, windowHeight)
N=1000

# Configuración de la fuente
font = pg.font.Font(None, 28)  # Puedes ajustar el tamaño y el estilo de la fuente

# Crear un objeto de texto
#text_lines = ["💾 s", "🗑️ d"]
text_lines = ["Save s", "Dump d"]
text_rendered = [font.render(line, True, (255, 255, 255)) for line in text_lines]  # Color blanco

# Posición del texto en la pantalla
text_rects = [text.get_rect(center=(windowWidth-40, (windowHeight // 2) + i * font.get_linesize())) for i, text in enumerate(text_rendered)]

#car = Car(road.getLaneCenter(1), windowHeight*0.90, 30, 50,"KEYS")
#car = Car(road.getLaneCenter(1), windowHeight*0.90, 30, 50,"AI")

def generateCars(N):
  cars = []
  for i in range(N):
    cars.append(Car(road.getLaneCenter(1), windowHeight*0.90,30,50,"AI"))
  return cars

cars = generateCars(N)
traffic = [
  Car(road.getLaneCenter(1), windowHeight*0.50, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(0), windowHeight*0.10, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(2), windowHeight*0.10, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(0), -windowHeight*0.20, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(1), -windowHeight*0.20, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(1), -windowHeight*0.50, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(2), -windowHeight*0.50, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(0), -windowHeight*0.80, 30, 50,"DUMMY", 2),
  Car(road.getLaneCenter(1), -windowHeight*0.80, 30, 50,"DUMMY", 2),
]

def getBrain(car, brain):
  for i in range(len(brain)):
    car.brain.levels[i].inputs = copy.deepcopy(brain[i]['inputs'])
    car.brain.levels[i].outputs = copy.deepcopy(brain[i]['outputs'])
    car.brain.levels[i].biases = copy.deepcopy(brain[i]['biases'])
    car.brain.levels[i].weights = copy.deepcopy(brain[i]['weights'])

def animate(t0, screen):

  bestCar = cars[0]

  bestCar.mainCar = True
  gameOn =True

  bestBrain = loadBestBrain()

  if len(bestBrain)!=0:
    for i in range(len(cars)):
      getBrain(cars[i], bestBrain)
      if(i!=0):
        NeuralNetwork.mutate(cars[i].brain,0.2)

  while gameOn:
    t1 = tm.perf_counter()
    deltaTime = t1-t0
    t0=t1
    road.update(bestCar.updateY)
    eventList = pg.event.get() #get all the events from the queue
    
    for event in eventList:
      if event.type == pg.KEYDOWN:
        if(event.key==pg.K_s):
          save(bestCar)
        if(event.key==pg.K_d):
          dump()
        if(event.key==pg.K_l):
          loadBestBrain()

    for i in range(0, len(traffic)):
      traffic[i].update(road.borders, [], [], bestCar.updateY)

    for car in cars:
      #best car condition election(fitness function)
      if bestCar.y > car.y:
        bestCar.mainCar = False
        bestCar = car
        bestCar.mainCar = True
      if np.abs(car.speed)<=0.1:
        car.quietCounter+=1
        if car.quietCounter>300:
          car.damaged=True
      else:
        car.quietCounter=0
      if gameOn:
        if(car.mainCar):
          gameOn = car.update(road.borders, traffic, eventList)
        else:
          if(not car.damaged):
            gameOn = car.update(road.borders, traffic, eventList, bestCar.updateY)
          if(car.damaged):
            cars.remove(car)


    # Limpia la pantalla
    screen.fill(black)
    left_surface.fill(backgroundGrey)
    right_surface.fill(black)

    road.draw(left_surface)
    for i in range(0, len(traffic)):
      traffic[i].draw(left_surface, red)
    
    for i in range(len(cars)):
      cars[i].draw(left_surface, blue)

    #pg.draw.circle(right_surface, (255, 255, 0), (windowWidth/2, windowHeight/2), 100)  # Dibuja un círculo amarillo


    # Dibuja el texto en la pantalla
    for text, rect in zip(text_rendered, text_rects):
      left_surface.blit(text, rect)

    Visualizer.drawNetwork(right_surface,bestCar.brain)
    # Copia las superficies en la pantalla principal
    screen.blit(left_surface, (0, 0))  # Superficie izquierda en la mitad izquierda de la pantalla
    screen.blit(right_surface, (windowWidth, 0))  # Superficie derecha en la mitad derecha de la pantalla

    pg.display.flip()

def save(bestCar):
  brain = []
  for level in bestCar.brain.levels:
    brainLevel = {
      'inputs': level.inputs,
      'outputs': level.outputs,
      'biases': level.biases,
      'weights': level.weights,
    }
    brain.append(brainLevel)
  with open("bestBrain.json", "w") as file:
    json.dump(brain, file)
    print("New brain saved")

def dump():
  fileName = "bestBrain.json"
  if os.path.exists(fileName):
    os.remove(fileName)
    print("Deleted file")
  else:
    print("File doesn't exists")

def loadBestBrain():
  fileName = "bestBrain.json"
  if os.path.exists(fileName):
    with open(fileName, "r") as json_file:
      data = json.load(json_file)
      print("Best brain loaded")
      return data
  else:
    print("There's no saved brain")
    return []


animate(tm.perf_counter(), screen) 