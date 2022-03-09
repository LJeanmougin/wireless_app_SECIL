import socket

BLUETOOTH = 0
WIFI = 1

class WirelessTalker:

    def __init__(self, protocol):
        self.protocol = protocol
    
    def filesize(self, file_name):
        file = open(file_name, "r")
        file.seek(0,2)
        size = file.tell()
        file.close()
        return size
    
    def sendfile(self, file_name, client):
        size = str(self.filesize(file_name))
