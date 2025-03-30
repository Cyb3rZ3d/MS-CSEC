#!/usr/bin/env python3
import fcntl
import struct
import os
from scapy.all import *
import time

# Constants for TUN interface setup
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# Set up the TUN interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)  # Replace 'valdez' with your chosen prefix
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name:", ifname)

# Configure IP and bring up the interface
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

try:
    while True:
        # Read a packet from the TUN interface
        packet = os.read(tun, 2048)
        if packet:
            # Create an IP object from the packet data
            ip = IP(packet)
            
            # Check if the packet is an ICMP echo request (ping request)
            if ip.haslayer(ICMP) and ip[ICMP].type == 8:  # ICMP Echo Request
                print("Received ICMP Echo Request:", ip.summary())
                
                # Construct an ICMP echo reply
                reply = IP(src=ip.dst, dst=ip.src) / ICMP(type=0, id=ip[ICMP].id, seq=ip[ICMP].seq) / ip[Raw].load
                os.write(tun, bytes(reply))  # Send the echo reply through the TUN interface
                print("Sent ICMP Echo Reply:", reply.summary())

except KeyboardInterrupt:
    print("\nProgram interrupted.")
    # Bring down the interface and close TUN
    os.system("ip link set dev {} down".format(ifname))
    os.close(tun)
