import zmq
import sys
from random import seed
from random import randint
import time
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);

seed(1)

context = zmq.Context()

s = context.socket(zmq.REQ)
s.connect('tcp://25.43.87.34:5555')

name = sys.argv[1]

for _ in range(10):
    value = randint(0, 10)
    message = name + ' ' + str(value)
    s.send_string(message)
    m = s.recv_string()
    print('Recibido ' + m)
    time.sleep(value)