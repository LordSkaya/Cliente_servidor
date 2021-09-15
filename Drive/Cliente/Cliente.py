import zmq #provee la comunicacion a traves de socket (hulk)
import sys
import json
import os
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL); 
#recibe las interacciones por teclado de manera asincrona

context = zmq.Context() #black box !!

#Crear un socket y lo conecta a traves del protocolo tcl con
#el puerto 8001

s = context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

username = sys.argv[1] #inputs
operacion = sys.argv[2]
try:
    nombrearchivo = sys.argv[3]
except:
    nombrearchivo = ""

data = "" #evita el programa tire un error por falta de "archivo"

if (operacion == "upload"): #evita que se lea el archivo localmente si no es operacion de subida
    with open(nombrearchivo,"r",encoding="utf8",errors="ignore") as f: #abre el archivo con el nombre enviado
        data = f.read() #lee el archivo
datos = {
    "username":username,
    "operacion":operacion,
    "nombrearchivo":nombrearchivo,
    "archivo":data #lo usamos para transformar data en un string
    }

rutaactual = os.path.dirname(os.path.abspath(__file__))

s.send_json(json.dumps(datos)) #dumps sirve para serializar. serializar: convertir un diccionario de python a json
m = s.recv_json()
mj = json.loads(m)

if (operacion == "download"): 
    ruta = os.path.join(rutaactual+"/descargas/", username)
    if(not os.path.exists(ruta)): #esto sirve para que no de error si se crean dos carpetas con el mismo nombre
        os.mkdir(ruta)
    with open(ruta+"/"+nombrearchivo, "w") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(mj["archivo"])
if (operacion == "downloadlink"):
    ruta = os.path.join(rutaactual+"/descargas/", username)
    if(not os.path.exists(ruta)): #esto sirve para que no de error si se crean dos carpetas con el mismo nombre
        os.mkdir(ruta)
    archivodescargado = mj["nombrearchivo"]
    with open(ruta+"/"+archivodescargado, "w") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(mj["archivo"])   
print (m)