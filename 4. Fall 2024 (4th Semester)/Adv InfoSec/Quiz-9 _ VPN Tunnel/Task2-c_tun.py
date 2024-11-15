#!/usr/bin/env python3

import fcntl
import struct
import os
import time
from scapy.all import *
import socket
from struct import pack

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Task 2.a: Modify the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

## Task 2.b: Configure the tun interface
"""
Added the provided code from the SeedLab doc
"""
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))


try:
    # Task 2.c: Read from the TUN Interface
    """
    Modifications made using SeedLab doc:
	- Added libraries import socket from struct import pack
	- removed the original 'while True' code and replaced it with whats written below.
    """
    while True:
    # Get a packet from the tun interface
        packet = os.read(tun, 2048)
        if packet:
            ip = IP(packet)
            print(ip.summary())
    

        
 
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting gracefully.")
finally:
    os.close(tun)
    print("Tun interface closed.")
