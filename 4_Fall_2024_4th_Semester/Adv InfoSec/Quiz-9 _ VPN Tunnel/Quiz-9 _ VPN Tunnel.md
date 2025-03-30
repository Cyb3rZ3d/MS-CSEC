Ruben Valdez <br> 
CSEC 5327 | Advanced InfoSec  <br> 
Prof. Izzat Alsmadi  <br> 
Tuesday’s@ 7pm  <br> 

# ***Quiz 9 - VPN Tunnel***

<br><br>

# Lab Setup

- The following are commands I took downloading the Labsetup.zip file from the VPN Tunneling lab page on SEED Labs 2.0:

        cd ~/Documents/AdvInfoSec
        
        mkdir VPNtunneling_Quiz-9
        
        cd VPNtunneling_Quiz-9
        
        curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/VPN_Tunnel/Labsetup.zip
        
        unzip Labsetup.zip

    ![alt text](<Screenshot 2024-11-09 at 7.10.22 AM.png>)


- Preliminary Docker maintenance to prune any and all prior running or down containers:

        docker-compose down --remove-orphans

        docker system prune -a --volumes

    ![alt text](<Screenshot 2024-11-09 at 7.54.46 AM.png>)

<br>

# Task 1: Network Setup

1. Building and starting the docker network:

    Build the network using 
        
        `sudo docker-compose build`

    Start the containers using 
    
        `sudo docker-compose up`

    ![alt text](<Screenshot 2024-11-09 at 10.18.22 AM.png>)


2. Opened a new terminal and remoted into each container.

    - Labs network diagram:
        ![alt text](<Screenshot 2024-11-09 at 10.32.24 AM.png>)

    - Remoted into each container in the network and ran `ifconfig` to gather additional network details:

            sudo docker exec -it client-10.9.0.5 /bin/bash
            sudo docker exec -it host-192.168.60.5 /bin/bash
            sudo docker exec -it host-192.168.60.6 /bin/bash
            sudo docker exec -it host-192.168.60.7 /bin/bash
            sudo docker exec -it server-router /bin/bash

        ![alt text](<Screenshot 2024-11-09 at 10.45.17 AM.png>)
        ![alt text](<Screenshot 2024-11-09 at 10.45.34 AM.png>)
        ![alt text](<Screenshot 2024-11-09 at 10.45.52 AM.png>)
        ![alt text](<Screenshot 2024-11-09 at 10.46.08 AM.png>)

    - Using `ping` I tested the network connections on the following containers and printed the results to `log.txt` file.

        - Host U

                ping 10.9.0.11 > log.txt

                cat log.txt

                ping 192.168.60.5 > log.txt

                cat log.txt

            ![alt text](<Screenshot 2024-11-09 at 10.59.10 AM.png>)
            
        - VPN Server

                ping 192.168.60.5 > log.txt

                cat log.txt

            ![alt text](<Screenshot 2024-11-09 at 10.59.58 AM.png>)


<br><br>


# Task 2: Create and Configure TUN Interface

1. Task 2a - Change the interface name from tun to valdez.

    Modified the provided .py script to complete this task.
    ![alt text](<Screenshot 2024-11-11 at 10.54.13 AM.png>)
    
    Changed the permission of the file to an executable and run the script:

        chmod a+x Task2-a.py
        ./Task2-a.py

    In a new terminal for `Host U`, I ran the command `ip address` to list a summary of the current network interfaces.  We can see the new interface I created `valdez0`.

    ![alt text](<Screenshot 2024-11-11 at 10.56.54 AM.png>)


2. Task 2b - Seting up the TUN Interface

    Building on top of the modified script from `Task2-a.py` and renamed it to `Task2-b.py`

    ![alt text](<Screenshot 2024-11-11 at 11.03.09 AM.png>)

    Changed the permission of the file to an executable and run the script:

        chmod a+x Task2-b.py
        ./Task2-a.py

    In the same secondary terminal used in `Task2-a`, I ran the command `ip address` to list a summary of the current network interfaces. The difference in appearance is that we can see IP details for the `valdez0` network interface.

    ![alt text](<Screenshot 2024-11-11 at 11.11.59 AM.png>)

3. Task 2.c - Read from the TUN Interface.  

    Continuation to build on `Task2-b.py` and renamed the script to `Task-2c.py`.  In this part of the code I modified the code to read packets and print IP summaries.

    Changed the permission of the file to an executable and run the script:

        chmod a+x Task2-b.py
        ./Task2-a.py
    
    In the same secondary terminal used in `Task2-a` and `Task2-b`, I ran the command `ip address` to list a summary of the current network interfaces. The difference in appearance is that we can see IP details for the `valdez0` network interface.
    
    ![alt text](<Screenshot 2024-11-11 at 1.30.24 PM.png>)

    Ping test:

    - On Host U, ping a host in the 192.168.53.0/24 network. What are printed out by the tun.py program? What has happened? Why?

        `ANSWER` After executing the script, I immediately noticed I was generating some kind of packets resulting in `Host U`.  After stopping the ping, I also noticed all the generated packets were lost. Another interesting issue I saw is that no packets were generated in Wireshark.

        ![alt text](<Screenshot 2024-11-11 at 1.38.42 PM.png>)
        ![alt text](<Screenshot 2024-11-11 at 1.38.10 PM.png>)

    - On Host U, ping a host in the internal network 192.168.60.0/24, Does tun.py print out anything? Why?

        `ANSWER` After running this ping, after executing the script and starting the ping, No packets were generating; although, in Wireshark I was seeing ICMP packets generating.  After stopping the ping, just like the above test packets were still lost. 

        ![alt text](<Screenshot 2024-11-11 at 1.41.23 PM.png>)
        ![alt text](<Screenshot 2024-11-11 at 1.40.39 PM.png>)
        ![alt text](<Screenshot 2024-11-11 at 1.40.09 PM.png>)


4. Task 2.d - Write to the TUN Interface
    
    Continuation to build on `Task2-c.py` and renamed the two scripts to `Task2-d1_tun.py`  and `Task2-d2_tun.py`.  I'll be using three (3) terminals (Term_1, Term_2, Term_3) for `Host U` to build the code, start the ping, and using Tshark.

    ***Step 1: `Task2-d1_tun.py`; Set Up the TUN Interface and Read Packets*** 
    
    `Term_1`:

    - Write an ICMP echo reply for ICMP echo requests.

        ![alt text](<Screenshot 2024-11-11 at 4.49.41 PM.png>)

    - Changed the permission of the file to an executable and run the script:

            chmod a+x Task2-b.py
            ./Task2-a.py

        ![alt text](<Screenshot 2024-11-11 at 4.52.09 PM.png>)
        ![alt text](<Screenshot 2024-11-11 at 4.52.30 PM.png>)
    
    `Term_2`:
    - 1st test:
        - ping 192.168.53.1
    - 2nd test:
        - ping 192.168.53.5

    `Term_3`"

    - Using `tcpdum` to capture packets within the docker network interface `valdez0`.  I attempted to use Wireshark and Tshark but wasn't able to install either application.

            tcpdump -i valdez0

        ![alt text](<Screenshot 2024-11-13 at 2.14.48 PM.png>)
        ![alt text](<Screenshot 2024-11-13 at 2.15.06 PM.png>)
        ![alt text](<Screenshot 2024-11-13 at 2.15.19 PM.png>)


    ***Step 2: `Task2-d2_tun.py` Send Arbitrary Data to the TUN Interface***

    - Tested how the system handles non-packet data, by temporarily modifying the code to send arbitrary data instead of an IP packet.

        ![alt text](<Screenshot 2024-11-12 at 8.50.06 AM.png>)

    - Changed the permission of the file to an executable and run the script:

            chmod a+x Task2-b.py
            ./Task2-a.py

        ![alt text](<Screenshot 2024-11-13 at 2.41.19 PM.png>)
        ![alt text](<Screenshot 2024-11-13 at 2.41.38 PM.png>)
        ![alt text](<Screenshot 2024-11-13 at 2.42.26 PM.png>)


# Task 3: Send the IP Packet to VPN Server Through a Tunnel

This task has two primary components:

- tun_client.py: Runs on Host U (the VPN Client) to capture packets from the TUN interface and send them to the VPN Server.

- tun_server.py: Runs on the VPN Server to receive packets from the client, extract the IP packet from the UDP payload, and print packet details.


## 3.1: Code for tun_server.py on the VPN Server

This server script `tun_server.py` listens on a specific UDP port to receive packets from the client. When a packet is received, the server extracts the IP packet from the UDP payload and prints the source and destination addresses.

- A UDP socket is created and bound to IP 0.0.0.0 and port 9090, allowing the server to listen on all network interfaces.
- For each packet received, the server extracts the IP packet and displays its source and destination IPs.

    ![alt text](<Screenshot 2024-11-09 at 11.02.29 PM.png>)

## 3.2: Code for tun_client.py on the VPN Client (Host U)

The client script `tun_client.py` captures packets from the TUN interface on Host U, wraps them in a UDP packet, and sends them to the VPN Server. This simulates tunneling the IP packets over a UDP connection.

- The script creates a TUN interface and assigns it an IP address of 192.168.53.99/24, bringing it up.

- A UDP socket is created, and the client captures packets from the TUN interface.

- Each packet is then sent to the VPN Server’s IP (10.9.0.11) and port (9090) over UDP.

    ![alt text](<Screenshot 2024-11-09 at 11.01.33 PM.png>)


## 3.3: Testing the Tunnel

Using x2 terminals for `Host U (VPN Client)`

- 1st terminal run the script

    ![alt text](<Screenshot 2024-11-09 at 11.14.20 PM.png>)

- 2nd terminal running the ping

    ![alt text](<Screenshot 2024-11-09 at 11.16.43 PM.png>)


`VPN Server (Router)`

![alt text](<Screenshot 2024-11-09 at 11.13.20 PM.png>)


## Explanation of How the Tunnel Works

- The client (Host U) captures packets on the TUN interface, treating them as IP packets intended for the private network.
- Each captured IP packet is then encapsulated inside a UDP packet by the client script and sent to the VPN Server.
- The server receives these UDP packets, extracts the original IP packet from the UDP payload, and displays its source and destination information.
- This setup simulates a basic VPN tunnel where IP packets are sent over a UDP connection to the server.
- This completes Task 3, establishing a one-way tunnel from the VPN Client to the VPN Server.


# Task 4: Set Up the VPN Server

In this task, I'll be taking a step-by-step approach with modifying some each sub-task.

## 4.1: Verify and confirm IP forwarding is enabled

Verified and confirmed IP forwarding was enabled in the `docker-compose.yml` file.  

    nano docker-compose.yml

![alt text](<Screenshot 2024-11-10 at 4.31.03 PM.png>)


## 4.2: Modify the script `tun_server.py` to write to the TUN interface

***`Router (VPN Server) 10.9.0.11`***

- Update the `tun_server.py` so that when the script is executed it does the following:

    - The server creates a TUN interface and assigns it the IP address 10.9.0.1/24.
    - A UDP socket listens on port 9090 to receive packets from the VPN Client.
    - When a packet is received, it is written to the TUN interface (os.write(tun, data)), making the kernel treat it as if it originated from the TUN interface. This allows the VPN Server’s routing table to forward the packet to its destination in the private network.

        ![alt text](<Screenshot 2024-11-10 at 4.55.43 PM.png>)

- The following commands were executed to modify the code, change modification permissions, and executing the code:
        
        nano tun_server_1.py
        chmod a+x tun_server_1.py
        ./tun_server_1.py

    ![alt text](<Screenshot 2024-11-10 at 4.56.36 PM.png>)

## 4.3: Testing the tunnel with forwarding

***`Host U (VPN Client) 10.9.0.5` _ 1st Terminal***

- Run the tun_client.py script on Host U.


***`Host U (VPN Client) 10.9.0.5` _ 2nd Terminal***

- Open a new terminal and attempt to ping an IP address in the private network of the VPN Server (e.g., 192.168.60.5).

        ping 192.168.60.5


***`Router (VPN Server) 10.9.0.11` _ 1st Terminal***

Make sure to run and execute the `./tun_server_1.py` script 


***`Router (VPN Server) 10.9.0.11` _ 2nd Terminal***

- Run tcpdump on the VPN Server to monitor traffic and ensure that ICMP packets reach Host V.

        sudo tcpdump -i valdez0 icmp


The following screenshots are in summary:

***`Host U (VPN Client) 10.9.0.5` _ 1st Terminal***

![alt text](<Screenshot 2024-11-10 at 5.24.05 PM.png>)

***`Host U (VPN Client) 10.9.0.5` _ 2nd Terminal***

![alt text](<Screenshot 2024-11-10 at 5.24.38 PM.png>)

***`Router (VPN Server) 10.9.0.11` _ 1st Terminal***

![alt text](<Screenshot 2024-11-10 at 5.25.05 PM.png>)

***`Router (VPN Server) 10.9.0.11` _ 2nd Terminal***

![alt text](<Screenshot 2024-11-10 at 5.25.19 PM.png>)

***Wireshark packets***

![alt text](<Screenshot 2024-11-10 at 5.27.56 PM.png>)

***NOTE***
Running the ping, I notice that ALL packets were lost and not received.  This confirm's `Host U` can send packets to the VPN server, which forwards them to their destination in the private network completing the one-way tunnel from `Host U` to `Host V`.


# Task 5: Handling Traffic in Both Directions

Task 4 was setting up one directional traffic.  At somepoint or another because the lab up to this point was dropping the packets.  In this task we will setup bi-directional traffic.  Meaning we'll be setting up two interface reading traffic.  

## 5.1 Modify `tun_server_2.py` to Handle Bidirectional Traffic

- Updated and modified the `tun_server_2.py` script on the VPN Server to:
    - Monitor both the TUN interface and UDP socket simultaneously.
    - Forward packets received on the TUN interface to the VPN Client.
    - Process packets received on the UDP socket as IP packets and inject them into the TUN interface.

- Commands to modify, change modification permissions, and executing the code:
        
        nano tun_server_2.py
        chmod a+x tun_server_2.py
        ./tun_server_2.py

    ![alt text](<Screenshot 2024-11-10 at 8.30.32 PM.png>)

    ![alt text](<Screenshot 2024-11-10 at 8.31.36 PM.png>)


## 5.2 Modify `tun_client_1.py` to Handle Bidirectional Traffic

- Updated and modified the `tun_client_1.py` script on the VPN Client (Host U):
    - Monitor both the TUN interface and the UDP socket.
    - Forward packets received on the TUN interface to the VPN Server over UDP.
    - Process packets received on the UDP socket as IP packets and inject them into the TUN interface.


- Commands to modify, change modification permissions, and executing the code:
        
        nano tun_client_1.py
        chmod a+x tun_client_1.py
        ./tun_client_1.py







<br><br>

# ***======Extra Credit======***

# Task 6: Tunnel-Breaking Experiment


# Task 7: Routing Experiment on Host V


# Task 8: VPN Between Private Networks


# ask 9: Experiment with the TAP Interface


# Summary



==============================================================
Tasks Redo
==============================================================


ip route add 192.168.53.99/24 dev valdez0 via 192.168.60.11

![alt text](<Screenshot 2024-11-13 at 9.00.59 PM.png>)