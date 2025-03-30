#!/usr/bin/env python3

import socket
import os
import fcntl
import struct
import select
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

IP_A = "0.0.0.0"  # Listen on all available interfaces
PORT = 9090       # UDP port to listen on
CLIENT_IP = "10.9.0.11"  # IP of the VPN Client

# Create the TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print(f"Interface Name: {ifname}")

# Configure the TUN interface
os.system("ip addr add 10.9.0.1/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

print("VPN Server is running and listening on port", PORT)

try:
    while True:
        # Use select to monitor both TUN interface and UDP socket
        ready, _, _ = select.select([sock, tun], [], [])

        for fd in ready:
            if fd is sock:
                # Received a packet from the VPN Client
                data, (client_ip, client_port) = sock.recvfrom(2048)
                print(f"Received packet from {client_ip}:{client_port}")

                # Write the packet to the TUN interface
                os.write(tun, data)
                print("Packet written to TUN interface")

            if fd is tun:
                # Received a packet from the TUN interface
                packet = os.read(tun, 2048)
                if packet:
                    ip = IP(packet)
                    print(f"Captured packet from TUN interface: {ip.src} --> {ip.dst}")

                    # Forward the packet to the VPN Client
                    sock.sendto(packet, (CLIENT_IP, PORT))
                    print("Packet sent to VPN Client")

except KeyboardInterrupt:
    print("\nShutting down VPN Server...")

finally:
    # Cleanup: close socket and TUN interface
    sock.close()
    os.close(tun)
    print("Resources released. Server shutdown complete.")
