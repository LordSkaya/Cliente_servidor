import zmq
import json

context = zmq.Context ()


s = context.socket(zmq.REP) 
s.bind('tcp://*:8001') #protocol://*:puerto
# el * es un rejects admite cualquier host.

def calculadora(arg):
    resultado = 0

    if arg["op"] == "mas":
        resultado = arg["x"] + arg["y"]
    elif arg["op"] == "menos":
        resultado = arg["x"] - arg["y"]
    elif arg["op"] == "por":
        resultado = arg["x"] * arg["y"]
    elif arg["op"] == "dividido":
        resultado = arg["x"] / arg["y"]
    elif arg["op"] == "raiz":
        resultado = arg["x"] ** (1/arg["y"])
    else:
        resultado = "Error"
    return resultado

while True:

    m = s.recv_json()
    var = json.loads(m)
    resultado = calculadora(var)
    s.send_string(str(resultado))
