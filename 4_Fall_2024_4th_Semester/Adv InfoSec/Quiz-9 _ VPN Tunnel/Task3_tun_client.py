#!/usr/bin/env python3

import fcntl
import struct
import os
import time
from scapy.all import *
import socket
from struct import pack


#Task3: Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_IP, SERVER_PORT = 10.9.0.11, 9090


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

# Task 2.b: Configure the tun interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# Task 3:  Sending data to another computer using UDP can be done using the standard socket programming.
try:
    while True:
        # Get a packet from the tun interface
        packet = os.read(tun, 2048)
        if packet:
            # Send the packet via the tunnel
            sock.sendto(packet, (SERVER_IP, SERVER_PORT))


except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting gracefully.")
finally:
    os.close(tun)
    print("Tun interface closed.")
