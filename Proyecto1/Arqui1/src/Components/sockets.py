#pip install websockets
#python sockets.py     (esto es para iniciar el servidor websockets)

import asyncio
import websockets
import json
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://3031142310108:x2HzFt2GmLiz1pZ0@proyecto1.3labb.mongodb.net/?retryWrites=true&w=majority&appName=Proyecto1"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#obtener la hora actual
import datetime
now = datetime.datetime.now()
#en una variable se guarda la hora actual con formato de 24 horas y en otra la fecha en formato dd-mm-aaaa
hora = now.strftime("%H:%M:%S")
fecha = now.strftime("%d/%m/%Y")
#Se accede a la base de datos
db = client['Sensores']
#Se accede a la coleccion
collection = db['sensores']

# Crear la consulta para filtrar los documentos del "Sensor temperatura"
query_tempt = {"Sensor": "Sensor temperatura"}
query_luz = {"Sensor": "Sensor luz"}
query_air = {"Sensor": "Sensor aire acondicionado"}
query_ingreso = {"Sensor": "Ingreso casa"}
query_tanque = {"Sensor": "Nivel agua"}

projection_tempt_fecha = {"Fecha": 1, "_id": 0}
projection_temp_hora = {"hora": 1, "_id": 0}

documents_tempt_fecha = collection.find(query_tempt, projection_tempt_fecha)
documents_tempt_hora = collection.find(query_tempt, projection_temp_hora)


projection_luz_fecha = {"Fecha": 1, "_id": 0}
projection_luz_hora = {"hora": 1, "_id": 0}

documents_luz_fecha = collection.find(query_luz, projection_luz_fecha)
documents_luz_hora = collection.find(query_luz, projection_luz_hora)

projection_air_fecha = {"Fecha": 1, "_id": 0}
projection_air_hora = {"hora": 1, "_id": 0}

documents_air_fecha = collection.find(query_air, projection_air_fecha)
documents_air_hora = collection.find(query_air, projection_air_hora)

projection_ingreso_fecha = {"Fecha": 1, "_id": 0}
projection_ingreso_hora = {"hora": 1, "_id": 0}

documents_ingreso_fecha = collection.find(query_ingreso, projection_ingreso_fecha)
documents_ingreso_hora = collection.find(query_ingreso, projection_ingreso_hora)

projection_tanque_fecha = {"Fecha": 1, "_id": 0}
projection_tanque_hora = {"hora": 1, "_id": 0}

documents_tanque_fecha = collection.find(query_tanque, projection_tanque_fecha)
documents_tanque_hora = collection.find(query_tanque, projection_tanque_hora)


projection_tempt = {"valor": 1, "_id": 0}
projection_luz = {"valor": 1, "_id": 0}
projection_air = {"valor": 1, "_id": 0}
projection_ingreso = {"valor": 1, "_id": 0}
projection_tanque = {"valor": 1, "_id": 0}



contador_tempt = 0
contador_luz = 0
contador_air = 0
contador_ingreso = 0
contador_tanque = 0

def read_temperature():
    global contador_tempt
    global temperature

    documents_tempt = collection.find(query_tempt, projection_tempt)
    # Ejecutar la consulta con proyección
    documents_tempt_fecha = collection.find(query_tempt, projection_tempt_fecha)
    documents_tempt_hora = collection.find(query_tempt, projection_temp_hora)

    documents_tempt = list(documents_tempt)
    documents_tempt_fecha = list(documents_tempt_fecha)
    documents_tempt_hora = list(documents_tempt_hora)

    if contador_tempt < len(documents_tempt):

        temperature = documents_tempt[contador_tempt]['valor']
        fecha = documents_tempt_fecha[contador_tempt]['Fecha']
        hora = documents_tempt_hora[contador_tempt]['hora']

        print("temperature;  contador: "+ str(contador_tempt) + " valor: " + str(temperature))

        if type(temperature)  != float: #string
            temperature = int(temperature.replace('°', '').replace(' C', '').strip())
            contador_tempt += 1
            
        else:  # float
            contador_tempt += 1
           

        return {
            "temperature":temperature,
            "fecha": fecha+" "+hora
            
        }
    else:
       
        return {
            "temperature":"",
            "fecha": ""
            
        }

def read_light():
    global contador_luz

    documents_luz = collection.find(query_luz, projection_luz)
    documents_luz_fecha = collection.find(query_luz, projection_luz_fecha)
    documents_luz_hora = collection.find(query_luz, projection_luz_hora)
    documents_luz = list(documents_luz)
    documents_luz_fecha = list(documents_luz_fecha)
    documents_luz_hora = list(documents_luz_hora)

    if contador_luz < len(documents_luz):

        luz = documents_luz[contador_luz]['valor']
        fecha = documents_luz_fecha[contador_luz]['Fecha']
        hora = documents_luz_hora[contador_luz]['hora']

        contador_luz += 1
        print("luz;  contador: "+ str(contador_luz) + " valor: " + str(luz))
            

        return {
            "light":luz,         
            "fecha": fecha+" "+hora
            
        }
    else:
        
        return {
            "light":"",         
            "fecha": ""
            
        } 
    
def read_air():
    global contador_air

    documents_air = collection.find(query_air, projection_air)
    documents_air_fecha = collection.find(query_air, projection_air_fecha)
    documents_air_hora = collection.find(query_air, projection_air_hora)
    documents_air = list(documents_air)
    documents_air_fecha = list(documents_air_fecha)
    documents_air_hora = list(documents_air_hora)

    if contador_air < len(documents_air):

        air = documents_air[contador_air]['valor']
        fecha = documents_air_fecha[contador_air]['Fecha']
        hora = documents_air_hora[contador_air]['hora']

        contador_air += 1
        print("air;  contador: "+ str(contador_air) + " valor: " + str(air))
            

        return {
            "air":air,         
            "fecha": fecha+" "+hora
            
        }
    else:
        
        return {
            "air":"",         
            "fecha": ""
            
        }
    
def read_ingreso():
    global contador_ingreso

    print("ESTOY EN INGRESO, contador ingreso: "+str(contador_ingreso))

    documents_ingreso = collection.find(query_ingreso, projection_ingreso)
    documents_ingreso_fecha = collection.find(query_ingreso, projection_ingreso_fecha)
    documents_ingreso_hora = collection.find(query_ingreso, projection_ingreso_hora)
    documents_ingreso = list(documents_ingreso)
    documents_ingreso_fecha = list(documents_ingreso_fecha)
    documents_ingreso_hora = list(documents_ingreso_hora)

    if contador_ingreso < len(documents_ingreso):

        ingreso = documents_ingreso[contador_ingreso]['valor']
        fecha = documents_ingreso_fecha[contador_ingreso]['Fecha']
        hora = documents_ingreso_hora[contador_ingreso]['hora']

        contador_ingreso += 1
        print("ingreso;  contador: "+ str(contador_ingreso) + " valor: " + str(ingreso))
            

        return {
            "ingreso":ingreso,          
            "fecha": fecha+" "+hora
                         
        }
    else:
        
        return {
            "ingreso":"",         
            "fecha": ""
            
        }

def read_tanque():
    global contador_tanque

    documents_tanque = collection.find(query_tanque, projection_tanque)
    documents_tanque_fecha = collection.find(query_tanque, projection_tanque_fecha)
    documents_tanque_hora = collection.find(query_tanque, projection_tanque_hora)
    documents_tanque = list(documents_tanque)
    documents_tanque_fecha = list(documents_tanque_fecha)
    documents_tanque_hora = list(documents_tanque_hora)

    if contador_tanque < len(documents_tanque):

        tanque = documents_tanque[contador_tanque]['valor']

        if tanque == "Alto":
            tanque = 1
        else:
            tanque = 0    

        fecha = documents_tanque_fecha[contador_tanque]['Fecha']
        hora = documents_tanque_hora[contador_tanque]['hora']

        contador_tanque += 1
        print("tanque;  contador: "+ str(contador_tanque) + " valor: " + str(tanque))
            

        return {
            "tanque":tanque,          
            "fecha": fecha+" "+hora
            
        }
    
    else:
        
        return {
            "tanque": "",        
            "fecha": ""
        } 
    
    
        

# Función que maneja las conexiones WebSocket y envía los datos de los sensores
async def sensor_data(websocket, path):
    
    while True:

        temperature_data = read_temperature()
        light_data = read_light()
        air_data = read_air()
        ingreso_data = read_ingreso()
        tanque_data = read_tanque()


        sensor_data = {
            'temperature': temperature_data,
            'light': light_data,
            'air': air_data,
            'ingreso': ingreso_data,
            'tanque': tanque_data
        }
        #temperature.temperature
        #temperature.fecha
        
        await websocket.send(json.dumps(sensor_data))
        await asyncio.sleep(2)  # Envía datos cada 2 segundos
        

# Configura y arranca el servidor WebSocket
start_server = websockets.serve(sensor_data, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()