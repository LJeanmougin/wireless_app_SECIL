#!/usr/bin/env python3

import sys
from wireless_listener import *
from wireless_talker import *

if __name__ == "__main__":
    
    if len(sys.argv) != 4 :
        print("Usage" + sys.argv[0] + ": protocol send/receive config_file")
        exit(1)
    protocol = sys.argv[1]
    role = sys.argv[2]
    config = sys.argv[3]
    if protocol == "bluetooth":
        protocol = BLUETOOTH
    elif protocol == "wifi":
        protocol = WIFI
    else :
        print("Protocole inconnu (bluetooth/wifi)")
        exit(2)
    if role == "send":
        device = WirelessTalker(protocol, config)
    elif role == "receive":
        device = WirelessListener(protocol, config)
    else :
        print("Role inconnu (send/receive)")
        exit(3)
    device.connect()
    device.communicate()
    device.close_communication()
    exit(0)