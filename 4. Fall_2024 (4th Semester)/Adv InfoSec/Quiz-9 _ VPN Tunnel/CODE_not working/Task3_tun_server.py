import socket
from scapy.all import *
import os

# Server IP and Port
IP_A = "0.0.0.0"  # Bind to all available interfaces
PORT = 9090

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))
print(f"Server listening on {IP_A}:{PORT}")

try:
    while True:
        # Receive data from the client
        data, (client_ip, client_port) = sock.recvfrom(2048)
        print(f"Received packet from {client_ip}:{client_port}")

        # Interpret data as an IP packet
        pkt = IP(data)
        print(f"Inside: {pkt.src} --> {pkt.dst}")
        
except KeyboardInterrupt:
    print("\nServer interrupted. Closing socket.")
    sock.close()
