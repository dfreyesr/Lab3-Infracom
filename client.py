import socket
import hashlib
import threading
from datetime import datetime
import os
import time

def log(archivo, cliente, tiempo, confirmacion):
        nombreLog = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'-log.txt'
        size = os.path.getsize(archivo)
        with open(nombreLog, 'a+') as f:
            f.write(f'Archivo: {archivo} size: {size} cliente {cliente} tiempo: {str(tiempo)} ms tuvo resultado {confirmacion}.\n')

def client(ip, port, nClient, nConexiones):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.sendall(b'listo')
    nombreArchivo = f'Cliente{nClient}-Prueba-{nConexiones}.txt'
    f = open(nombreArchivo,'wb+')
    start = time.time()
    l = s.recv(1024)
    while (l):
        f.write(l)
        l = s.recv(1024)
        if(l.decode('utf8')=='fin'):
            break
    end = time.time()
    hash = s.recv(1024)
    f.close()
    print('Hash compare i')
    hashCompare = hashlib.md5(open(nombreArchivo,'rb').read()).hexdigest()
    print('Hash compare f')
    if(hash.decode('utf8') == hashCompare):
        confirmacion = 'success'
        s.sendall(b'success')
    else:
        confirmacion = 'fail'
        s.sendall(b'fail')
    s.close()
    log(nombreArchivo, nClient, end-start, confirmacion)

nConexiones = int(input('Ingrese el número de clientes: '))
for x in range(nConexiones):
    th = threading.Thread(target=client, args=('127.0.0.1',65432, x, nConexiones))
    th.start()