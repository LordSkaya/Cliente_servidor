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
    with open(ruta+"/"+nombrearchivo, "wb") as f: #abre el archivo, crear el archivo copiando el que se le fue enviado
        f.write(archivo)
    respuesta = [b"archivo guardado con exito"]
    s.send_multipart(respuesta)

def download(username, nombrearchivo):
    ruta = os.path.join(rutaactual+"/archivos/", username)
    with open(ruta+"/"+nombrearchivo,"rb") as f:
        descarga = f.read()
    respuesta = [descarga]
    s.send_multipart(respuesta)

def sharelink(username, nombrearchivo):
    ruta = rutaactual+"/archivos/"+username+"/"+nombrearchivo
    respuesta = [ruta.encode("utf-8")] 
    s.send_multipart(respuesta)

def downloadlink(link):
    nombrearchivo = link.split("/")[-1] #es para coger el ultimo argumento de la lista es decir despues del ultimo "/", el ultimo argumento de llista
    with open(link,"rb") as f:
        descarga = f.read()
    respuesta = [descarga,nombrearchivo.encode("utf-8")]
    s.send_multipart(respuesta)

def listar(username):
    ruta = rutaactual+"/archivos/"+username
    archivoslistados = os.listdir(ruta)
    respuesta = [archivoslistados.encode("utf-8")]
    s.send_multipart(respuesta)


def opciones(datos):
    operacion = datos[1].decode("utf-8")
    if(operacion == "upload"):
        upload(datos[0].decode("utf-8"),datos[2].decode("utf-8"),datos[3]) 
    elif(operacion == "download"):
        download(datos[0].decode("utf-8"),datos[2].decode("utf-8"))
    elif(operacion == "sharelink"):
        sharelink(datos[0].decode("utf-8"),datos[2].decode("utf-8"))
    elif(operacion == "downloadlink"):
        downloadlink(datos[2].decode("utf-8"))
    elif(operacion == "listar"):
        listar(datos[0].decode("utf-8"))

while True:
    print ("Esperando peticion")
    m = s.recv_multipart()
    opciones(m)
