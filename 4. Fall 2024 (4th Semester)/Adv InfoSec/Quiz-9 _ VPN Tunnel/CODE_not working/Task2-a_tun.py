#!/usr/bin/env python3
import fcntl
import struct
import os
import time

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'valdez%d', IFF_TUN | IFF_NO_PI)  # Replace 'tun' with your last name
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name:", ifname)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("\nProgram interrupted.")
    os.close(tun)
