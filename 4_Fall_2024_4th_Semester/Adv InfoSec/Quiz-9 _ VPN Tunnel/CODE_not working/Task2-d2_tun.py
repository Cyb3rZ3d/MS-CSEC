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
            ip = IP(packet)

            # Check if the packet is an ICMP echo request (type 8)
            if ip.haslayer(ICMP) and ip[ICMP].type == 8:  # ICMP Echo Request
                print("Received ICMP Echo Request:", ip.summary())
                
                # Send arbitrary data instead of an IP packet
                arbitrary_data = b"Hello, this is arbitrary data!"
                os.write(tun, arbitrary_data)
                print("Sent arbitrary data:", arbitrary_data)

except KeyboardInterrupt:
    print("\nProgram interrupted.")
    # Bring down the interface and close TUN
    os.system("ip link set dev {} down".format(ifname))
    os.close(tun)