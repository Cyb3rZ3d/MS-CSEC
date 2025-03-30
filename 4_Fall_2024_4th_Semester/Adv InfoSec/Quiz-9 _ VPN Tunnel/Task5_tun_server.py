#!/usr/bin/env python3
import fcntl
import struct
import os
import time
from scapy.all import *

# tun interface
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

# Configure the tun interface
os.system("ip addr add 192.168.53.11/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# UDP Server
IP_A = "0.0.0.0"
PORT = 9090

ip,port = "10.9.0.5", 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

try:
    while True:
        # this will block until at least one interface is ready
        ready,_,_ = select.select([sock,tun],[],[])

        for fd in ready:
            if fd is sock:
                data, (ip,port) = sock.recvfrom(2048)
                print("From UDP {}:{} --> {}:{}".format(ip,port, IP_A,PORT))
                pkt = IP(data)
                print("From socket (IP) ==>: {} --> {}".format(pkt.src, pkt.dst))
                # ... (code needs to be added by students) ...
                os.write(tun, bytes(pkt))

            if fd is tun:
                packet = os.read(tun,2048)
                pkt = IP(packet)
                print("From tun ==>: {} --> {}".format(pkt.src, pkt.dst))
                # ... (code needs to be added by students) ...
                sock.sendto(packet, (ip,port))

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting gracefully.")
finally:
    os.close(tun)
    print("Tun interface closed.")