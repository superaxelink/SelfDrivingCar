import numpy as np
import utils as ut
class NeuralNetwork:

  def __init__(self, neuronCounts):
    self.levels=[]
    for i in range(len(neuronCounts)-1):
      self.levels.append(Level(neuronCounts[i],neuronCounts[i+1]))
    
  @staticmethod
  def feedForward(givenInputs, network):
    outputs = Level.feedForward(givenInputs,network.levels[0])
    for i in range(1, len(network.levels)):
      outputs = Level.feedForward(outputs, network.levels[i])
    return outputs

  @staticmethod
  def mutate(network, amount=1):
    for level in network.levels:
      for i in range(len(level.biases)):
        level.biases[i] = ut.lerp(level.biases[i], np.random.random()*2-1,amount)

      for i in range(len(level.weights)):
        for j in range(len(level.weights[i])):
          level.weights[i][j] = ut.lerp(level.weights[i][j], np.random.random()*2-1,amount)

class Level:
  def __init__(self, inputCount, outputCount):
    self.inputs = [0]*inputCount #initialize inputs, outputs, biases, and weights
    self.outputs = [0]*outputCount
    self.biases = [0]*outputCount

    self.weights = []

    for i in range(0, inputCount):
      self.weights.append([0]*outputCount)

    self.randomize(self)
  
  def randomize(self, level):
    for i in range(0, len(level.inputs)):
      for j in range(0, len(level.outputs)):
        level.weights[i][j] = np.random.random()*2 - 1 #add random weights between -1 and 1

    for i in range(len(level.biases)):
      level.biases[i] = np.random.random()*2-1 #add random biases between -1 and 1
        #self.inputs = np.zeros(inputCount)

  @staticmethod
  def feedForward(givenInputs, level):
    for i in range(0, len(level.inputs)):
      level.inputs[i] = givenInputs[i] #update inputs with previous inputs
    
    for i in range(0, len(level.outputs)):
      sum = 0
      for j in range(0, len(level.inputs)):
        sum += level.inputs[j]*level.weights[j][i]
      
      if(sum>level.biases[i]):
        level.outputs[i] = 1
      else:
        level.outputs[i] = 0
    
    return level.outputs