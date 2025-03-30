#!/usr/bin/env python3
import fcntl
import struct
import os
import socket
from scapy.all import *

# Constants for TUN setup
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# Server IP and Port
SERVER_IP = "192.168.60.11"  # Replace with VPN Server's IP
SERVER_PORT = 9090

# Set up the TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)  # Replace 'valdez' with your prefix
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name:", ifname)

# Configure IP and bring up the interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# Create UDP socket for sending packets to the VPN server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Read a packet from the TUN interface
        packet = os.read(tun, 2048)
        if packet:
            ip = IP(packet)
            print(f"Read packet from TUN interface: {ip.src} --> {ip.dst}")
            
            # Send the packet to the server via UDP
            sock.sendto(packet, (SERVER_IP, SERVER_PORT))
            print(f"Sent packet to server at {SERVER_IP}:{SERVER_PORT}")

except KeyboardInterrupt:
    print("\nClient interrupted. Closing socket and TUN interface.")
    os.system("ip link set dev {} down".format(ifname))
    os.close(tun)
    sock.close()




