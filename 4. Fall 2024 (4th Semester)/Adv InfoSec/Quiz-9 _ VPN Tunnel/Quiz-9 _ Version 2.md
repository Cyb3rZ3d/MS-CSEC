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
        
        ![alt text](<Screenshot 2024-11-14 at 7.14.26 PM.png>)
        ![alt text](<Screenshot 2024-11-14 at 7.15.30 PM.png>)
        ![alt text](<Screenshot 2024-11-14 at 7.15.15 PM.png>)

---
---
---

# Task 3: Send the IP Packet to VPN Server Through a Tunnel

The following bullets will be outlined as a chronological order of running different terminals:

1. `router|10.9.0.11-192.168.60.11`; 1st Terminal

    - Created and saved the script `Task3_tun_server` using nano, changed permissions using `chmod a+x`, and executing the scription using `./`.

        ![alt text](<Screenshot 2024-11-14 at 8.55.13 PM.png>)

2. `Host-U|10.9.0.5`; 2nd Terminal

    - Created and saved the script `Task3_tun_client` using nano, changed permissions using `chmod a+x`, and executing the scription using `./`.    

        ![alt text](<Screenshot 2024-11-14 at 8.59.01 PM.png>)

3. `Host-U|10.9.0.5`; 3rd Terminal 
    
    - Running tcpdump sniffing the `valdez0` interface.

            tcpdump -i valdez0

4. `Host-U|10.9.0.5`; 4th Terminal

    1. Ping a IP in the network of 192.168.53.0/24

            ping 192.168.53.5 -c 2


5.  ***Sub-Task Questions***

    1. To test whether the tunnel works or not, ping any IP address belonging to the 192.168.53.0/24 network.  What is printed out on VPN Server? Why?

        After pinging the IP address `192.168.53.5` I saw traffic getting captured but were getting dropped becuase the IP getting ping was a fake IP and not a live IP.   

        `router|10.9.0.11-192.168.60.11`; 1st Terminal <br> ![alt text](<Screenshot 2024-11-14 at 9.13.02 PM.png>)

        `Host-U|10.9.0.5`; 2nd Terminal <br> ![alt text](<Screenshot 2024-11-14 at 9.16.54 PM.png>)

        `Host-U|10.9.0.5`; 3rd Terminal  <br> ![alt text](<Screenshot 2024-11-14 at 9.17.40 PM.png>)

        `Host-U|10.9.0.5`; 4th Terminal <br> ![alt text](<Screenshot 2024-11-14 at 9.17.15 PM.png>)

    2. Let us ping Host V, and see whether the ICMP packet is sent to VPN Server through the tunnel. If not, what are the problems?
        
        - `Host-U|10.9.0.5`; 3rd Terminal
            - Add an entry to the routing table:  `ip route add 192.168.60.0/24 dev valdez0`
            - ping 192.168.60.5:    `ping 192.168.60.5 -c 2`

            ![alt text](<Screenshot 2024-11-14 at 9.42.19 PM.png>)

        - `router|10.9.0.11-192.168.60.11`; 1st Terminal <br> ![alt text](<Screenshot 2024-11-14 at 9.43.05 PM.png>)

            - Here we can clearly see the packets are encapsulated.   

---
---
---

# Task 4: Set Up the VPN Server

1. Per the instruction requirements, create a script `Task4_tun_server.py` to complete the following:

    - Create a TUN interface and configure it.
    - Get the data from the socket interface; treat the received data as an IP packet.
    - Write the packet to the TUN interface.

        ![alt text](<Screenshot 2024-11-14 at 10.55.01 PM.png>)

2. Secondly, I also needed to create another script names `Task4_tun_client.py` IP forwarding (routing):

    ![alt text](<Screenshot 2024-11-14 at 10.57.10 PM.png>)

3. In a chronological order, I'll list out the tasks completed:

    1. `Host-V|192.168.60.5`; 1st Terminal

        - Start tcpdump <br>    ![alt text](<Screenshot 2024-11-14 at 11.02.54 PM.png>)

    2. `router|10.9.0.11-192.168.60.11`; 2nd Terminal

        - Verify and confirm the new network interface was created  <br>    ![alt text](<Screenshot 2024-11-14 at 11.04.16 PM.png>)

    3. `router|10.9.0.11-192.168.60.11`; 3rd Terminal

        - Change permissions to execute and run the script  <br>    ![alt text](<Screenshot 2024-11-14 at 11.06.00 PM.png>)

    4. `Host-U|10.9.0.5`; 4th Terminal

        - Change permissions to execute and run the `Task4_tun_client.py` script  <br>  ![alt text](<Screenshot 2024-11-14 at 11.07.40 PM.png>)

4.  ***Sub-Task Questions***

    After running bother scripts I'm able to see captured traffic filtering in on `Host-V|192.168.60.5`.

---
---
---

# Task 5: Handling Traffic in Both Directions

Next steps will be provided chronologically.  

1. Created two scripts named `Task5_tun_server.py` and `Task5_tun_client.py`.

    - changed each script's permissions and executed them using the following commands:

            chmod a+x Task5_tun_server.py
            chmod a+x Task5_tun_client.py

2. `router|10.9.0.11-192.168.60.11`; 1st Terminal executing Task5_tun_server.py
    
    ![alt text](<Screenshot 2024-11-15 at 1.19.15 AM.png>)
    ![alt text](<Screenshot 2024-11-15 at 1.17.56 AM.png>)

3. `Host-U|10.9.0.5`; 2nd Terminal executing Task5_tun_client.py

    ![alt text](<Screenshot 2024-11-15 at 1.20.41 AM.png>)
    ![alt text](<Screenshot 2024-11-15 at 1.20.02 AM.png>)

4. `Host-U|10.9.0.5`; 3rd Terminal starting tcpdump

    ![alt text](<Screenshot 2024-11-15 at 1.21.11 AM.png>)

5. `Host-V|192.168.60.5`; 4th Terminal starting tcpdump

    ![alt text](<Screenshot 2024-11-15 at 1.21.46 AM.png>)


6. `Host-U|10.9.0.5`; 5th Terminal using ping, `ping 192.168.60.5 -c 2`

    ![alt text](<Screenshot 2024-11-15 at 1.22.04 AM.png>)

7. ***Sub-Task Questions***

    1. From the above step's 1-6, i was successfully able to ping `Host-V|192.168.60.5`.  The output from each image provide the commands needed and the output from the ping shows that inbound/outbound traffic is getting captured on unsecurity vpn.  

    2. After pinging `Host-V|192.168.60.5`  I was successfully able to telnet into this machine using the credentials `UN: seed | Pwd: dees`.

        - `Host-U|10.9.0.5`; 5th Terminal   <br>    ![alt text](<Screenshot 2024-11-15 at 1.24.14 AM.png>)

        - `Host-V|192.168.60.5`; 4th Terminal   <br>  ![alt text](<Screenshot 2024-11-15 at 1.33.40 AM.png>)

        








