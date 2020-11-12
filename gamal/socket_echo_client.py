import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Datos del Client (emisor del mensaje)
# Valor B del emisor
b = 15
# Mensaje
txt = open("mensajeentrada.txt","r")
m = txt.read()
txt.close()

mascii = []
for i in m:
    mascii.append(ord(i))

m = mascii
try:
    

    # Look for the response
    amount_received = 0

    while amount_received <= 0:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))
    ms = data.decode("utf-8")  #mensaje de server
    
    if len(ms.split(","))== 3:
        try:
            g = int(ms.split(",")[0])
            p = int(ms.split(",")[1])
            k = int(ms.split(",")[2])
            
            y1 = (g**b)%p
            y2 = []
            for i in m:
                y2.append(((k**b)*i)%p)
            
            # Enviamos mensaje
            message = bytes((str(y1)+"|"+str(y2)), 'utf-8')
            
            print('sending {!r}'.format(message))
            sock.sendall(message)
        except:
            pass
    else:
        print("Ha ocurrido un error al recivir la clave publica")

finally:
    print('closing socket')
    sock.close()
