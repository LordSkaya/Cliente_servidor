import zmq
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);

context = zmq.Context()

x = context.socket(zmq.REP) # Reply
x.bind('tcp://*:5555')

i = 0
while True:
    m = x.recv_string()
    print('Servidor recibe ' + m)
    x.send_string(m)
    i = i + 1
    print("Se atendio el mensaje {}".format(i))