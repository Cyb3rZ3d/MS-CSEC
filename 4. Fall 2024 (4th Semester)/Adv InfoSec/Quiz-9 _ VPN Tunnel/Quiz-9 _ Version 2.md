# Task 1: Network Setup

1. 

2. 

3. 

***Task 1 lab testing Questions:***

1. Host U can communicate with VPN Server.

    `ANSWER:` I'm able to ping both router's public and private networks. Using tcpdump I'm able to sniff the network traffic of of the ping request.

    - `Host-U|10.9.0.5`; 1st Terminal:

            ping 10.9.0.11 -c 2
            ping 192.168.60.11 -c 2

        ![alt text](<Screenshot 2024-11-13 at 11.58.47 PM.png>)
        ![alt text](<Screenshot 2024-11-13 at 11.59.12 PM.png>)

    - `Host-U|10.9.0.5`; 2nd Terminal:

            tcpdump -i eth0

        ![alt text](<Screenshot 2024-11-14 at 12.18.44 AM.png>)

2. VPN Server can communicate with Host V.

    `ANSWER:` 
    - When running the ping, and capturing traffic i noticed the following on each interface:

        - `eth0 - 10.9.0.1`; packets were lost.
        - `eth1 - 192.168.60.11`; packet's were received. 

    - `router|10.9.0.11-192.168.60.11`; 1st Terminal

        ![alt text](<Screenshot 2024-11-14 at 12.33.34 AM.png>)

    - `Host-U|10.9.0.5`; 2nd Terminal:

            tcpdump -i eth0

        ![alt text](<Screenshot 2024-11-14 at 12.31.29 AM.png>)



3. Host U should not be able to communicate with Host V.

    - `Host-U|10.9.0.5`; 1st Terminal:

            ping 192.168.60.5 -c 2

        ![alt text](<Screenshot 2024-11-13 at 11.40.37 PM.png>)

    - `Host-U|10.9.0.5`; 2nd Terminal:

            tcpdump -i eth0

        NOTE: All traffic from prior pings have breaks of empty spaces.  
        ![alt text](<Screenshot 2024-11-13 at 11.41.18 PM.png>)

4. Run tcpdump on the router, and sniff the traffic on each of the network.  Show that you can capture packets.

    `ANSWER`:   The network diagram shows there's five (5) systems but when I run `docker-compose ps` I can only see there are four (4) systems; client, server, and two (2) host's.  The only last IP to ping is `192.168.60.6`.  The IP `192.168.60.7` is null.

    ![alt text](<Screenshot 2024-11-14 at 12.55.33 AM.png>)
    
    - `router|10.9.0.11-192.168.60.11`; 1st Terminal using `ping`

        - ping 192.168.60.6 -c 2

            ![alt text](<Screenshot 2024-11-14 at 12.45.07 AM.png>)

    - `router|10.9.0.11-192.168.60.11`; 2nd Terminal using `tcpdump`
        
        - Capturing the ping traffic
            
            ![alt text](<Screenshot 2024-11-14 at 12.44.40 AM.png>)

---
---
---

# Task 2: Create and Configure TUN Interface

## Task 2.a: Name of the Interface

Two (2) terminals were opened for `Host-U|10.9.0.5:`

1. `Host-U|10.9.0.5`; 1st Terminal

    - Modifified the code to rename the network interface name from `tun0` to `valdez0`.

    - Accessed the `tun.py` script in the `~/volumes` folder using nano and saved as `Task2-a_tun.py`.  The following are commands used to open and save the script:

            nano tun.py
            chmod a+x Task2-a_tun.py
            ./Task2-a_tun.py

        ![alt text](<Screenshot 2024-11-14 at 1.14.56 AM.png>)

2. `Host-U|10.9.0.5`; 2nd Terminal

    - Ran `ip addr` to verify and confirm the network interface `valdez0` was added

        ![alt text](<Screenshot 2024-11-14 at 1.22.18 AM.png>)


## Task 2.b: Set up the TUN Interface assigning an IP and to start it

1. `Host-U|10.9.0.5`; 1st Terminal
    
    - Modifified the code by adding what is highlighted in this screenshot to set up the TUN Interface by assigning an IP address and to bring it up.

        ![alt text](<Screenshot 2024-11-14 at 10.03.49 AM.png>)

    - Accessed the `Task2-a_tun.py` script in the `~/volumes` folder using nano and saved as `Task2-a_tun.py`.  The following commands were used to open and save the script:

            nano Task2-a_tun.py
            chmod a+x Task2-a_tun.py
            ./Task2-a_tun.py
        
        ![alt text](<Screenshot 2024-11-14 at 10.05.22 AM.png>)

2. `Host-U|10.9.0.5`; 2nd Terminal

    - Ran `ip addr` to verify and confirm the network interface `valdez0` was added
        
        ![alt text](<Screenshot 2024-11-14 at 10.06.34 AM.png>)

3. ***Explaination in difference***
The only difference from 2a and 2b is that in 2b, we assigned an IP address and brought it up and online "global".

## Task 2.c: Read from the TUN Interface

1. `Host-U|10.9.0.5`; 1st Terminal running the script
    
    - Modifified the code by adding what is highlighted in this screenshot to set up the TUN Interface by assigning an IP address and to bring it up.

        ![alt text](<Screenshot 2024-11-14 at 12.48.25 PM.png>)

    - Accessed the `Task2-a_tun.py` script in the `~/volumes` folder using nano and saved as `Task2-a_tun.py`.  The following commands were used to open and save the script:

            nano Task2-a_tun.py
            chmod a+x Task2-a_tun.py
            ./Task2-a_tun.py
        
        ![alt text](<Screenshot 2024-11-14 at 10.05.22 AM.png>)

2. `Host-U|10.9.0.5`; 2nd Terminal running the ping

    - Ran `ip addr` to verify and confirm the network interface `valdez0` to gather network interface details and to `ping 192.168.153.5 -c 2`

        ![alt text](<Screenshot 2024-11-14 at 3.29.06 PM.png>)

3. `Host-U|10.9.0.5`; 3rd Terminal running tcpdump sniffing the `valdez0` interface.

    ![alt text](<Screenshot 2024-11-14 at 1.14.34 PM.png>)

4. ***Sub-Task Questions***
    1. On Host U, ping a host in the 192.168.53.0/24 network. What are printed out by the tun.py program? What has happened? Why?
    
    `Answer`:   Ping'ing `192.168.53.5` resulted in packet loss.  This reason is because the IP isn't a live host.  It's a random IP within the subnet I decided to choose.
    
    2. On Host U, ping a host in the internal network 192.168.60.0/24, Does tun.py print out anything? Why?

        When I pinged `192.168.60.5` I received packet loss on the 1st Terminal but received no traffic on the 2nd terminal like I originally did on the 1st ping.  On the 3rd Terminal, running tcpdump, I didn't receive any traffic.  I the reason no traffic was being transmitted is because I haven't set up communication is only within the subnet of this network 192.168.53.0/24.
    

## Task 2.d: Write to the TUN Interface


1. `Host-U|10.9.0.5`; 1st Terminal running the script

    - Accessed the `Task2-c_tun.py` script in the `~/volumes` folder using nano and saved as `Task2-d_tun.py`.  The following commands were used to open and save the script:

            nano Task2-c_tun.py
            chmod a+x Task2-a_tun.py
            ./Task2-d_tun.py

        ![alt text](<Screenshot 2024-11-14 at 4.18.30 PM.png>)

        ![alt text](<Screenshot 2024-11-14 at 10.05.22 AM.png>)

        ![alt text](<Screenshot 2024-11-14 at 4.22.40 PM.png>)

2. `Host-U|10.9.0.5`; 2nd Terminal running the ping

    ![alt text](<Screenshot 2024-11-14 at 4.20.23 PM.png>)

3. `Host-U|10.9.0.5`; 3rd Terminal running tcpdump sniffing the `valdez0` interface.

    ![alt text](<Screenshot 2024-11-14 at 4.21.31 PM.png>)

4. ***Sub-Task Questions***

    - After getting a packet from the TUN interface, if this packet is an ICMP echo request packet, construct a corresponding echo reply packet and write it to the TUN interface. Please provide evidence to show that the code works as expected.

    - Instead of writing an IP packet to the interface, write some arbitrary data to the interface, and report your observation.

        Answering both these questions in single response.  Here I was able to set write script that injects a request/reply and then spoofing the response with a non-existent system. 
        

---
---
---

# Task 3: Send the IP Packet to VPN Server Through a Tunnel























