import random
import time
import paho.mqtt.client as mqtt
import json
import numpy

minRange = 20.0 # min temp range for temp. simulation
maxRange = 27.0 # max temp range for temp. simulation

indexCounter = 0

def genTemperature(minRange,maxRange):
  temp = random.randint(minRange, maxRange)
  return temp

def formatTemperature(sensorId):
#génération d'une chaîne JSON pour l'envoi à MQTT
  data = {}
  data['sensorID'] = 'sensor-' + str(sensorId)
  data['type'] = 'temperature'
  data['value'] = genTemperature(minRange,maxRange)
  return data

def generateNodes(numNodes):
#Génération des capteurs de température
  objs = [mqtt.Client() for i in range(numNodes)]
  for i in range(numNodes):
    objs[i].connect("localhost", 1883, 60)
    objs[i].loop_start()
  return objs