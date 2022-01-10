import json
import paho.mqtt.client as mqtt


tempArr = [None] * 3 # Tableau pour sauvegarder les moyennes des capteurs
average = ""
setPoint = 22 # Température désirée
tempControlArr = [] # Variable pour sauvegarder les températures
sampingInterval = 3 # Intervalle par defaut avant d'effectuer les calculs

def on_connect(client, userdata, rc,properties=None):
    print("Connected with result code "+str(rc))
    client.subscribe("/readings/temperature")

def on_message(client, userdata, msg):
    print(str(msg.payload))
    calculateAverage(client,msg.payload)

def calculateAverage(client, message):
#Calculer la moyenne et la transmettre via JSON
    if not any(v is None for v in tempArr): #Voir si on à toutes les températures
        average = sum(tempArr) / len(tempArr) # Calculer la moyenne des températures d'une chambre
        tempControl(client, average) # Appliquer la méthode de controle de température
        for i in range(0,len(tempArr)):
            tempArr[i] = None # Vider la liste des températures

    data = json.loads(message)
    sensorNumber = data["sensorID"].split("-")
    tempArr[ int(sensorNumber[1]) ] = int(data["value"]) # Remplir le tableau avec l'identifiant des capteurs

def tempControl(client, currTemperature):
    global sampingInterval
    global setPoint
    data = {}
    if(len(tempControlArr) != sampingInterval):
        tempControlArr.append(currTemperature)
    else:
        currTemperature = sum(tempControlArr) / len(tempControlArr)
        print(currTemperature)
        del tempControlArr[:]

        if((currTemperature >= 26) or(currTemperature <= 20) ): # Si température anormale, data['level']=1
            data['level'] = 1
        else:
            data['level'] = 0
        print(json.dumps(data))
        client.publish("/actuators/room-1", json.dumps(data)) # Publication des données avec MQTT