#!/usr/bin/env python3

import socket
from scapy.all import *


# Server IP and Port
IP_A = "0.0.0.0"  # Listen on all interfaces
PORT = 9090       # Port for receiving packets

# Create a UDP socket and bind to IP and Port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))
print(f"Listening on {IP_A}:{PORT} for incoming packets.")

try:
    
    while True:
        # Receive packet from the client
        data, (ip, port) = sock.recvfrom(2048)
        print(f"Received packet from {ip}:{port}")
        pkt = IP(data)  # Interpret received data as IP packet
        print(" Inside Packet: {} --> {}".format(pkt.src, pkt.dst))

except KeyboardInterrupt:
    print("\nServer interrupted. Shutting down gracefully...")
finally:
    sock.close()
    print("Socket closed. Exiting program.")
