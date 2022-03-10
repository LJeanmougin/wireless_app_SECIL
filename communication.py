import sys
from wireless_listener import *
from wireless_talker import *

if __name__ == "__main__":
    
    if len(sys.argv) != 3 :
        print("Usage" + sys.argv[0] + ": protocol send/receive")
        exit(1)
    protocol = sys.argv[1]
    role = sys.argv[2]
    if protocol == "bluetooth":
        protocol = BLUETOOTH
    elif protocol == "wifi":
        protocol = WIFI
    else :
        print("Protocole inconnu (bluetooth/wifi)")
        exit(2)
    if role == "send":
        device = WirelessTalker(protocol)
    elif role == "receive":
        device = WirelessListener(protocol)
    else :
        print("Role inconnu (send/receive)")
        exit(3)
    device.connect()
    device.communicate()
    device.close_communication()
    exit(0)