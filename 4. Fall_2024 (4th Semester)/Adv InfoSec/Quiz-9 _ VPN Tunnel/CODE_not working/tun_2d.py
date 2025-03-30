#!/usr/bin/env python3
import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# Task 2.a: Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")

# Task 2.b: Configure the TUN interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

print("Interface Name: {}".format(ifname))

try:
    # Task 2.c: Read from the TUN Interface
    while True:
        # Get a packet from the tun interface
        packet = os.read(tun, 2048)
        if packet:
            ip = IP(packet)
            print(ip.summary())

            # Task 2.d: Check if the packet is an ICMP echo request
            if ip.proto == 1 and ip[ICMP].type == 8:  # ICMP type 8 is echo request
                # Construct the echo reply packet
                newip = IP(src=ip.dst, dst=ip.src)
                newicmp = ICMP(type=0)  # ICMP type 0 is echo reply
                newpkt = newip / newicmp / ip.payload
                os.write(tun, bytes(newpkt))
                print("Sent ICMP echo reply")

except KeyboardInterrupt:
    print("\nGracefully shutting down.")
    
finally:
    os.close(tun)
