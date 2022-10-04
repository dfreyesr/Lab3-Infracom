from socketserver import ThreadingTCPServer,StreamRequestHandler
import threading
import hashlib
from datetime import datetime
import time
import os

class echohandler(StreamRequestHandler):
    def log(self, archivo, cliente, tiempo, confirmacion):
        nombreLog = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'-log.txt'
        size = os.path.getsize(archivo)
        with open(nombreLog, 'a+') as f:
            f.write(f'Archivo: {archivo} size: {size} cliente {cliente[0]}:{cliente[1]} tiempo: {str(tiempo)} ms tuvo resultado {confirmacion}.\n')

    def handle(self):
        print(f'Connected: {self.client_address[0]}:{self.client_address[1]}')
        nConexiones = self.server.nConexiones
        archivo = self.server.archivo
        hashS = self.server.hash
        while True:
            activeClients = threading.activeCount() - 1
            if(activeClients == nConexiones):
                msg = self.request.recv(1024)
                if(msg.decode('utf8') == 'listo'):
                    f = open (archivo, "rb")     
                    start = time.time()               
                    l = f.read(1024)
                    print('Enviando info')
                    while (l):
                        self.request.send(l)
                        l = f.read(1024)
                    print('Fin info')
                    self.request.send(b'fin')
                    end = time.time()
                    self.request.send(hashS)
                    confirmacion = self.request.recv(1024).decode('utf8')
                    self.log(archivo, self.client_address, end-start, confirmacion)
                    self.server.shutdown()
                    break

nConexiones = int(input('Ingrese el número de conexiones que desea: '))
archivo = input('Ingrese el archivo que desea enviar: ')
server = ThreadingTCPServer(('',65432), echohandler)
server.hash = hashlib.md5(open(archivo,'rb').read()).hexdigest().encode('utf8')
server.nConexiones = nConexiones
server.archivo = archivo
server.serve_forever()