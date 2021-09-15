import zmq #provee la comunicacion a traves de socket (hulk)
import sys
import json

context = zmq.Context() #black box !!

#Crear un socket y lo conecta a traves del protocolo tcl con
#el puerto 8001

s = context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

x = int(input())
op = input()
y = int(input())


datos = {"x":x, "y":y, "op":op} #diccionario "llave": "valor"

s.send_json(json.dumps(datos))
m = s.recv_string()
print (m)
