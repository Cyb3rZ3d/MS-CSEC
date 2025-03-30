***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 4 - `hydra_telnet.pcap` and `nmap.pcap` <br>
Due: Feb. 20, 2025 <br>



Went to `https://packettotal.com` and uploaded the following pcaps:

```
hydra_telnet.pcap
nmap.pcap
```

![alt text](<Screenshot 2024-02-20 at 3.37.27 PM.png>)


# 1. hydra_telnet.pcap

## Network Graph

At first glance using the `Network Graph`, it appears there are a number of different connections.  I was able to apply filters for `Overlays` and enbale `Malicious Traffic` and `Suspicous Traffic`.  After applying the filters, I was able to identify the `Host and Link Details` and recognized there was a `Suspicious` Severity between `192.168.47.255` and `192.168.47.1`.

![alt text](<Screenshot 2024-02-20 at 3.44.18 PM.png>)


## Timeline Analysis

We can assert, using the `Timeline Analysis` feature, the time table for the suspicious activity took place in the late morning 11:48 AM between the following connections:

![alt text](<Screenshot 2024-02-20 at 3.51.13 PM.png>)


## Suspicious Traffic

Selecting filters  in suspicious traffic, i was able to filter threats `policy` and `suspicous`.  Not using any other filters.  The output, we can see there is a high severity for a policy suspecious for a `Potential Corporate Privacy Violation` alert dscription.  The details show the alert happened 5:48 AM using port 17500 / UDP.

![alt text](<Screenshot 2024-02-21 at 9.14.38 PM.png>)

![alt text](<Screenshot 2024-02-21 at 9.14.55 PM.png>)


## Hosts

Using the Hosts generic view, we can see all the hosts and the packets sent/received and the payloads sent/received.  The dashboard also shows the total hosts, packets, and the time of connections.

![alt text](<Screenshot 2024-02-21 at 10.19.23 PM.png>)

Filtering specific to Threats we can identifiy `192.168.47.1` having threats.

![alt text](<Screenshot 2024-02-21 at 10.17.04 PM.png>)


## Communications

In communications, we can see a better view of all the packets to further investigate into the traffic of the .pcap.   

Since the pcap is referring to `telnet`, I was able to filter for only TCP connections.  After initial reveiw, all the connections were to destination port 23 (telnet).

![alt text](<Screenshot 2024-02-21 at 10.41.15 PM.png>)

Filtering for threats, the only packet that shows is a connection between SRC `192.168.47.1` and DEST `192.168.47.255` on SRC/DEST port 17500.

![alt text](<Screenshot 2024-02-21 at 10.39.24 PM.png>)


## Artifacts

Unable to use this charm or section as the site page just turns white and nothing populates.   

<br >
<br >


# 2. Nmap.pcap


## Network Graph

Here is a graph filtering for overlays and graph analysis.  In the graph, we can see all the traffic specific within a minute time.  The traffic graph shows top talkers `192.168.75.132`,  `192.168.0.20`, and `192.168.75.255`.

![alt text](<Screenshot 2024-02-21 at 10.59.35 PM.png>)

![alt text](<Screenshot 2024-02-21 at 10.59.10 PM.png>)

![alt text](<Screenshot 2024-02-21 at 10.59.56 PM.png>)




## Timeline Analysis

We can assert there was a time span of 32 seconds of the number of total packets that were within this capture.  


![alt text](<Screenshot 2024-02-21 at 11.10.01 PM.png>)



## Suspicious Traffic

No suspicious traffic to report. 


## Hosts

Seeing that there are 4 hosts in this pcap that were communicating across the wire.  We can assert here in this table that there were a large number of sent/received packets deriving from `192.168.75.1` and `192.168.75.132` which does cause for concern there is alot of traffic being produced between these two hosts.   


![alt text](<Screenshot 2024-02-21 at 11.16.01 PM.png>)



## Communications

Here, I'm able to filter for connection state and I'm further able to filter IP `192.168.75.132` and see there are a number of connections to `192.168.0.20` on a number of different ports.   

![alt text](<Screenshot 2024-02-21 at 11.27.29 PM.png>)


![alt text](<Screenshot 2024-02-21 at 11.26.45 PM.png>)


![alt text](<Screenshot 2024-02-21 at 11.37.10 PM.png>)
