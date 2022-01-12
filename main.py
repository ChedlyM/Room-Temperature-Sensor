import Publisher as Publisher
import Subscriber as Subscriber
import time
import paho.mqtt.client as mqtt
import json
import _thread

def publisherStart():
  #Création de capteurs pour la prise de température et envoi des températures au brocker
  numNodes = 1 # Nombre de capteurs dans la chambre
  interval = 5 # Envoi des données chaque seconde (5)
  objs = Publisher.generateNodes(numNodes) # génération d'un tableau d'objets temporaires
  c=1
  #Tester le programme avec un certain nombre de traitement (10 fois par exemple)
  while(c<10):
    for i in range(numNodes):
      data = Publisher.formatTemperature(i) # Création d'une chaine Json
      objs[i].publish("/readings/temperature", json.dumps(data)) # Publication des données avec mqtt
    time.sleep(interval)
    c=c+1
  for client in objs:
    client.loop_stop(); client.disconnect()


def subscriberInit():
  #Initialisation du subscriber MQTT
    client = mqtt.Client()
    client.on_connect = Subscriber.on_connect
    client.on_message = Subscriber.on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()

def main():
    try:
        print("Lancement du Publisher")
        _thread.start_new_thread(publisherStart, () ) # Creation d'un thread publisher
        print("Lancement du Subscriber")
        _thread.start_new_thread(subscriberInit, () ) # Creation d'un thread subscriber
    except:
        print("Impossible de lancer les threads")
    while 1:
        pass
main()