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

data = b"" #evita el programa tire un error por falta de "archivo"

if (operacion == "upload"): #evita que se lea el archivo localmente si no es operacion de subida
    with open(nombrearchivo,"rb") as f: #abre el archivo con el nombre enviado
        data = f.read() #lee el archivo
datos = [username.encode("utf-8"),operacion.encode("utf-8"),nombrearchivo.encode("utf-8"),data] #estoy trasnformando el string a binario con la codificacion utf-8

rutaactual = os.path.dirname(os.path.abspath(__file__))

s.send_multipart(datos) 
m = s.recv_multipart()

if (operacion == "download"): 
    ruta = os.path.join(rutaactual+"/descargas/", username)
    if(not os.path.exists(ruta)): #esto sirve para que no de error si se crean dos carpetas con el mismo nombre
        os.mkdir(ruta)
    with open(ruta+"/"+nombrearchivo, "wb") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(m[0])
elif (operacion == "downloadlink"):
    ruta = os.path.join(rutaactual+"/descargas/", username)
    if(not os.path.exists(ruta)): #esto sirve para que no de error si se crean dos carpetas con el mismo nombre
        os.mkdir(ruta)
    archivodescargado = m[1].decode('utf-8')
    with open(ruta+"/"+archivodescargado, "wb") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(m[0])
else: 
    print (m)