#!/usr/bin/env python3
import socket
import os
from scapy.all import *

SERVER_IP = "10.9.0.11"  # IP address of the VPN Server
SERVER_PORT = 9090       # Port number the VPN Server listens on

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# Create the TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print(f"Interface Name: {ifname}")

# Configure the TUN interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("VPN Client is running and sending packets to the server...")

while True:
    # Capture a packet from the TUN interface
    packet = os.read(tun, 2048)
    if packet:
        ip = IP(packet)
        print(f"Captured packet: {ip.src} --> {ip.dst}")

        # Send the packet via UDP to the server
        sock.sendto(packet, (SERVER_IP, SERVER_PORT))
        print("Packet sent to VPN Server")
