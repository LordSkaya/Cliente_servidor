import zmq
import json
import os
import pathlib
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);
#recibe las interacciones por teclado de manera asincrona

context = zmq.Context ()


s = context.socket(zmq.REP) 
s.bind('tcp://*:8001') #protocol://*:puerto
rutaactual = str(pathlib.Path(__file__).parent.absolute())#da la ruta actual donde esta el script

def upload(username, nombrearchivo, archivo): #funcion que hace la subida del archivo

    ruta = os.path.join(rutaactual+"/archivos/", username) 
    if(not os.path.exists(ruta)): #esto sirve para que no de error si se crean dos carpetas con el mismo nombre
        os.mkdir(ruta) #crea la carpeta
    with open(ruta+"/"+nombrearchivo, "w", errors="ignore") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(archivo)
    respuesta = {
        "mensaje":"archivo guardado con exito"
    }
    s.send_json(json.dumps(respuesta))

def download(username, nombrearchivo):
    ruta = os.path.join(rutaactual+"/archivos/", username)
    with open(ruta+"/"+nombrearchivo) as f:
        descarga = f.read()
    respuesta = {
        "archivo":descarga
    }
    s.send_json(json.dumps(respuesta))

def sharelink(username, nombrearchivo):
    ruta = rutaactual+"/archivos/"+username+"/"+nombrearchivo
    respuesta = {
        "link":ruta
    }
    s.send_json(json.dumps(respuesta))

def downloadlink(link):
    nombrearchivo = link.split("/")[-1] #es para coger el ultimo argumento de la lista es decir despues del ultimo "/", el ultimo argumento de llista
    with open(link) as f:
        descarga = f.read()
    respuesta = {
        "archivo":descarga,
        "nombrearchivo":nombrearchivo
    }
    s.send_json(json.dumps(respuesta))

def listar(username):
    ruta = rutaactual+"/archivos/"+username
    archivoslistados = os.listdir(ruta)
    respuesta = {
        "archivoslistados":archivoslistados
    }
    s.send_json(json.dumps(respuesta))


def opciones(datos):
    operacion = datos["operacion"]
    if(operacion == "upload"):
        upload(datos["username"],datos["nombrearchivo"],datos["archivo"]) 
    elif(operacion == "download"):
        download(datos["username"],datos["nombrearchivo"])
    elif(operacion == "sharelink"):
        sharelink(datos["username"],datos["nombrearchivo"])
    elif(operacion == "downloadlink"):
        downloadlink(datos["nombrearchivo"])
    elif(operacion == "listar"):
        listar(datos["username"])

while True:
    print ("Esperando peticion")
    m = s.recv_json()
    mj = json.loads(m)
    opciones(mj)
