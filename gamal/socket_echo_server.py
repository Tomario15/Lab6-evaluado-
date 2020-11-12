import socket
import sys
import ast

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Datos del Server (receptor del mensaje)
# Primo
p = 107
# Generador
g = 64
# Valor A del receptor
a = 35
# Key
k = (g**a) % p

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        
        # Enviamos la clave publica
        print('Enviando la clave publica a client')
        Cb =bytes((str(g)+","+str(p)+","+str(k)), 'utf-8') #G,P,K
        print('sending {!r}'.format(Cb))
        connection.sendall(Cb)

        # Receive the data in small chunks
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                cm = data.decode("utf-8").split("|")
                
                if cm[1][len(cm[1])-1] != "]":
                    while True:
                        data = connection.recv(16)
                        print('reciviendo data adicional {!r}'.format(data))
                        if data:
                            cm[1]+= data.decode("utf-8")
                        else:
                            break
                    cm[1]= ast.literal_eval(cm[1])
                    
                try:
                    # Preparamos los datos recividos
                    y1 = int(cm[0])
                    y2 = cm[1]
                    
                    mtrad = ""
                    for j in y2:
                        m = ((y1**(p-1-a))*j)%p
                        mtrad += chr(m)
                        
                    txt = open("mensajerecibido.txt","w")
                    menEntrtxt = txt.write(mtrad+"\n")
                    txt.close()
                except:
                    print("ha ocirrido un error de formato")
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
