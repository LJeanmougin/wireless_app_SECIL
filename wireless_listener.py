import socket
import os

BLUETOOTH = 0
WIFI      = 1
TYPE_FILE = b'F'
TYPE_CMD  = b'C'

class WirelessListener:

    def __init__(self, protocol):
        self.protocol = protocol
        self.connection

    def connect(self):
        if self.protocol == WIFI:
            with open("./host_ip", "r") as ip_conf:
                addr = ip_conf.readline()[:-1]
            with open("./port", "r") as port_conf:
                port = int(port_conf.readline())
            socket_type = socket.AF_INET
        elif self.protocol == BLUETOOTH:
            port = 5
            with open("./host_macaddr", "r") as macaddr_conf:
                addr = macaddr_conf.readline()[:-1]
            socket_type = socket.AF_BLUETOOTH
        socket = socket.socket(socket_type, socket.SOCK_STREAM)
        socket.bind((addr, port))
        socket.listen(1)
        self.connection, client_addr = socket.accept()
        print("Connection address:", client_addr)
    
    def communicate(self):
        choice = 1
        while choice == 1:
            type = self.connection.recv(1)
            msg = self.connection.recv(1).decode("UTF-8")
            while msg[-1] != '\0':
                msg += self.connection.recv(1).decode("UTF-8")
            if type == TYPE_FILE:
                try:
                    size = self.connection.recv(1)
                    while size[-1] != '\0'.encode("UTF-8"):
                        size += self.connection.recv(1)
                    content = self.connection.recv(int(size[:len(size)-1]))
                    new_file = open(msg[:-1], 'wb')
                    new_file.write(content)
                    new_file.close()
                except:
                    print("Echec de l'ecriture du fichier")
            elif type == TYPE_CMD:
                try:
                    process = os.popen(msg[:-1])
                    print(process.read())
                except:
                    print("Echec de l'exécution de la commande")
            else:
                print("Paquet inconnu")
            print("Souhaitez vous rester en ligne ? :")
            print("1) Oui")
            print("2) Non")
            choice = int(input())
    
    def close_communication(self):
        self.connection.close()
