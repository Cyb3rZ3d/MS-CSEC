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

# Task 2.b: Configure the tun interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

try:
    # Task 2.c: Read from the TUN Interface
    while True:
        # Get a packet from the tun interface
        packet = os.read(tun, 2048)
        if packet:
            pkt = IP(packet)
            print("{}:".format(ifname), pkt.summary())

            # Task 2.d-1: If it's an ICMP echo request, create an echo reply
            if ICMP in pkt and pkt[ICMP].type == 8:  # ICMP type 8 is an echo request
                print("Original Packet:")
                print("Source IP:", pkt[IP].src)
                print("Destination IP:", pkt[IP].dst)

                # Construct an ICMP echo reply
                ip = IP(src=pkt[IP].dst, dst=pkt[IP].src, ihl=pkt[IP].ihl)
                icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)  # type 0 is an echo reply
                data = pkt[Raw].load if Raw in pkt else b''
                reply_pkt = ip / icmp / data

                print("Spoofed Echo Reply Packet:")
                print("Source IP:", reply_pkt[IP].src)
                print("Destination IP:", reply_pkt[IP].dst)

                # Write the echo reply to the TUN interface
                #os.write(tun, bytes(reply_pkt))

                # Task 2.d-2: Write arbitrary data to the TUN interface
                arbdata = b'***This is arbitrary test data***'
                print("Writing arbitrary data to the TUN interface:", arbdata)
                #os.write(tun, arbdata)

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting gracefully.")
finally:
    os.close(tun)
    print("Tun interface closed.")
