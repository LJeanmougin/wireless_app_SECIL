import yaml
import socket
import os

BLUETOOTH = 0
WIFI      = 1
TYPE_FILE = b'F'
TYPE_CMD  = b'C'

class WirelessListener():

    protocol = None
    connection = None
    config_file = None

    def __init__(self, protocol, config_file):
        
        self.protocol = protocol
        self.config_file = config_file

    def connect(self):

        yaml_config = open(self.config_file)
        config = yaml.load(yaml_config, Loader=yaml.FullLoader)
        print(config['host_ip'])
        if self.protocol == WIFI:
            addr = config['host_ip']
            port = int(config['ip_port'])
            socket_type = socket.AF_INET
        elif self.protocol == BLUETOOTH:
            addr = config['host_mac']
            port = int(config['bluetooth_port'])
            socket_type = socket.AF_BLUETOOTH
        server = socket.socket(socket_type, socket.SOCK_STREAM)
        server.bind((addr, port))
        server.listen(1)
        self.connection, client_addr = server.accept()
        print("Connection address:", client_addr)
    
    def communicate(self):
        choice = 1
        while choice == 1:
            type = self.connection.recv(1)
            b = self.connection.recv(1)
            msg = b.decode("UTF-8")
            while msg[-1] != '\0':
                b = self.connection.recv(1)
                msg += b.decode("UTF-8")
            if type == TYPE_FILE:
                try:
                    s = self.connection.recv(1)
                    size = s
                    while s != '\0'.encode("UTF-8"):
                        s = self.connection.recv(1)
                        size += s
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
