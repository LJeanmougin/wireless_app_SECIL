import socket

BLUETOOTH = 0
WIFI      = 1
TYPE_FILE = b'F'
TYPE_CMD  = b'C'

class WirelessTalker:

    def __init__(self, protocol):
        self.protocol = protocol
        self.client


    def connect(self):
        if self.protocol == WIFI:
            with open("./dest_ip", "r") as ip_conf:
                addr = ip_conf.readline()[:-1]
            with open("./port", "r") as port_conf:
                port = int(port_conf.readline())
            socket_type = socket.AF_INET
        elif self.protocol == BLUETOOTH:
            port = 5
            with open("./paired_macaddr", "r") as macaddr_conf:
                addr = macaddr_conf.readline()[:-1]
            socket_type = socket.AF_BLUETOOTH
        self.client = socket.socket(socket_type, socket.SOCK_STREAM)
        self.client.connect((addr, port))

    def filesize(file_name):
        file = open(file_name, "r")
        file.seek(0,2)
        size = file.tell()
        file.close()
        return size
    
    def sendfile(self, file_name):
        size = str(self.filesize(file_name))
        self.client.send(b'F') #header pour envoi de fichier
        self.client.send(bytes(file_name, 'utf-8'))
        self.client.send(b'\0')
        self.client.send(bytes(size, 'utf-8'))
        self.client.send(b'\0')
        file = open(file_name, "rb")
        self.client.send(file.read())
        file.close()
    
    def execremote(self, commande):
        self.client.send(b'C') #header pour commande
        self.client.send(bytes(commande, 'utf-8'))
        self.client.send(b'\0')

    def communicate(self):
        choice = 0
        while(choice != 3):
            choice = 0
            while choice != 1 and choice != 2 and choice != 3:
                print("Veuillez choisir une action :")
                print("1) Envoyer un fichier")
                print("2) Envoyer une commande")
                print("3) Quitter")
                choice = int(input())
            if choice == 1:
                print("Entrer le nom du fichier à envoyer :")
                nom_fichier = input()
                try:
                    self.sendfile(nom_fichier)
                except:
                    print("Echec de l'envoi")
            elif choice == 2:
                print("Entrer la commande à envoyer :")
                commande = input()
                try:
                    self.execremote(commande)
                except:
                    print("Echec de l'exécution")
    
    def close_communication(self):
        self.client.close()
                