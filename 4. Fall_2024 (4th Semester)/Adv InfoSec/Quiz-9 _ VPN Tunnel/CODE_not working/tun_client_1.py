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

SERVER_IP = "10.9.0.11"  # IP of the VPN Server
SERVER_PORT = 9090       # Port number the VPN Server listens on

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

try:
    while True:
        # Use select to monitor both TUN interface and UDP socket
        ready, _, _ = select.select([sock, tun], [], [])

        for fd in ready:
            if fd is sock:
                # Received a packet from the VPN Server
                data, (server_ip, server_port) = sock.recvfrom(2048)
                print(f"Received packet from {server_ip}:{server_port}")

                # Write the packet to the TUN interface
                os.write(tun, data)
                print("Packet written to TUN interface")

            if fd is tun:
                # Received a packet from the TUN interface
                packet = os.read(tun, 2048)
                if packet:
                    ip = IP(packet)
                    print(f"Captured packet from TUN interface: {ip.src} --> {ip.dst}")

                    # Forward the packet to the VPN Server
                    sock.sendto(packet, (SERVER_IP, SERVER_PORT))
                    print("Packet sent to VPN Server")

except KeyboardInterrupt:
    print("\nShutting down VPN Client...")

finally:
    # Cleanup: close socket and TUN interface
    sock.close()
    os.close(tun)
    print("Resources released. Client shutdown complete.")
