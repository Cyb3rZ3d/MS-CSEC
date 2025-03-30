***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Project 1 <br>
Due: Feb. 29, 2024 <br>

---

<br>

# Project 1 - Packet Snifing and Spoofing Lab


<br>

## Lab Setup

Using GCP, I created a GCP Ubuntu instance (34.29.142.101).

Using terminal, I was able to SSH into my instance to gain remote access to the instance.

Completed the following commands to efficiently run the lab:
    
```
    sudo apt install net-tools

    sudo apt install python3-pip

    pip3 install scapy
    
```

<br>

## Task 1.1A

- Using the provided code, I needed to verify and confirm my network interfaces so I could establish what interfaced to apply in this code:

    ![alt text](<Screenshot 2024-02-19 at 9.16.43 PM.png>)

- Using `ifconfig` to determine what my network interfaces were:

    ![alt text](<Screenshot 2024-02-19 at 9.18.18 PM.png>)

- Executed the scapy program `sniffer.py` using the command `sudo python3 sniffer.py`.  Following the command are the start of the results of the sent/received packets using ICMP.

    ![alt text](<Screenshot 2024-02-19 at 8.36.29 PM.png>)

- Started a ping scan to `www.google.com` testing ICMP connections to see if the target is communicating. 

    ![alt text](<Screenshot 2024-02-19 at 8.36.47 PM.png>)


<br>

## Task 1.1B

### Capture only the ICMP packets.

Using the provided sample, I completed the following commands in creating a new file named `sniffer_only_icmp.py`

![alt text](<Screenshot 2024-02-20 at 9.35.18 AM.png>)

<br>

#### Task 1.1B.1 | Troubleshooting issues with Wireshark

I was unable to locate a way to select the appropriate network capture. Troubleshooting the issue, I decided to just reinstall and reconfigure Wireshark. The following is derived using the history  command to list the commands used. Here you'll see the commands used to re-install, reconfigure, adding the user to the Wireshark group, and rebooting the GCP Ubuntu instance. After running the commands I was now able to successfully open Wireshark and see the available network captures I needed to complete the remainder of the task.

![alt text](<Screenshot 2024-02-19 at 10.02.32 PM.png>)

<br>

After rebuilding Wireshark, I was able to successfully run the `sniffer_only_icmp.py` script and then ping `www.google.com`.  Observing the network traffic using a ICMP filter. 

![alt text](<Screenshot 2024-02-20 at 9.29.36 AM.png>)

![alt text](<Screenshot 2024-02-20 at 9.30.00 AM.png>)

![alt text](<Screenshot 2024-02-20 at 9.41.38 AM.png>)

<br>

#### Task 1.1B.2 | Capture any TCP packet that comes from a particular IP and with a destination port number 23.

Created a script ``tcp_sniffer.py` and added source IP `10.128.0.2` to the code:

![alt text](<Screenshot 2024-02-20 at 11.51.15 AM.png>)


Made the script executable using the command `sudo chmod a+x tcp_sniffer.py`.


Gathered secondary system details from Kali Linux using `ifconfig`

![alt text](<Screenshot 2024-02-20 at 11.44.35 AM.png>)


Started a Telnet connection to destination IP `192.168.1.42`.

![alt text](<Screenshot 2024-02-20 at 11.59.13 AM.png>)


Started the Scapy script

![alt text](<Screenshot 2024-02-20 at 12.13.19 PM.png>)


Wireshark capture of the telnet connection

![alt text](<Screenshot 2024-02-20 at 11.26.01 AM.png>)


<br>

#### Task 1.1B.3 | Capture packets comes from or to go to a particular subnet.


In the CLI of my GCP Ubuntu instance, I created the file `subnet_sniffer.py` using `nano`.  

![alt text](<Screenshot 2024-02-29 at 3.03.37 PM.png>)


Using my VMware Kali VM, I used the command `ip addr show` to identify the `eth0` network subnet.

![alt text](<Screenshot 2024-02-20 at 1.20.05 PM.png>)


After starting the sniffer, I started to ping for the IP `192.168.1.42` and then tracking the network traffic using Wireshark. 

- sniffer

    ![alt text](<Screenshot 2024-02-29 at 3.07.39 PM.png>)

- ping

    ![alt text](<Screenshot 2024-02-29 at 3.08.03 PM.png>)

- Wireshark traffic

    ![alt text](<Screenshot 2024-02-29 at 3.08.26 PM.png>)


<br>
<br>

### Task 1.2: Spoofing ICMP Packets

After reading the instructions I first attempting to use my own IP parameters using a VMware Kali VM `192.168.1.42` and my GCP instance IP `10.128.0.2`. 

- Starting the sniffer using Python3 and pinging for ICMP packets using the destination IP

    ![alt text](<Screenshot 2024-02-29 at 3.45.24 PM.png>)

    ![alt text](<Screenshot 2024-02-29 at 3.45.55 PM.png>)


- Wireshark results show identify the number of ICMP packets requested.  Only thing here is that i do not see and replies.  

    ![alt text](<Screenshot 2024-02-29 at 3.47.23 PM.png>)

    ***Note: The only request and reply packets that were observed were from a different task not associated to this assignment.  I just kept the capture running w/o stopping.   So i'm not to sure what those packets were for.***


<br>
<br>

### Task 1.3: Traceroute

Analyzing the code for Task 1.3, I decided to use a different IP instead of the provided IP.  What I ended up doing was a nslookup for google.com.  Using the IP, `209.85.146.102`, I was able to created the python script to complete the traceroute using scapy.  The following will show the number of hopes completed during the traceroute and the wireshark results.  

- `nslookup google.com`

    ![alt text](<Screenshot 2024-02-29 at 8.37.51 PM.png>)

- python script `task-1.3.py`

    ![alt text](<Screenshot 2024-02-29 at 8.43.08 PM.png>)

- Execution and starting of the scapy python script `task-1.3.py`

    ![alt text](<Screenshot 2024-02-29 at 8.44.27 PM.png>)

- Wireshark results of the network traffic when executing the traceroute

    ![alt text](<Screenshot 2024-02-29 at 8.46.45 PM.png>)


<br>
<br>


### Task 1.4: Snifing and-then Spoofing

So to be able to switch this part of the project up, i decided to use the dedicated SEED Labs provided docker images.   

Imported the lab setup environment using the following command: 
    
`curl -O https://seedsecuritylabs.org/Labs_20.04/Files/Sniffing_Spoofing/Labsetup.zip`


Started and built the docker-compose environment:

![alt text](<Screenshot 2024-02-29 at 10.56.07 PM.png>)

Remoted into each machine using the following commands:

    - seed-attacker-10.9.0.1

        `sudo docker exec -it seed-attacker bash`

    - hostA-10.9.0.5

        `sudo docker exec -it hostA-10.9.0.5 bash`

    - hostB-10.9.0.6

        `sudo docker exec -it hostB-10.9.0.6 bash`



In the `seed-attacker-10.9.0.1` machine, I created the python script, made it an executable, and then ran the script.

![alt text](<Screenshot 2024-02-29 at 11.10.15 PM.png>)

![alt text](<Screenshot 2024-02-29 at 11.00.58 PM.png>)


In host `hostA-10.9.0.5`, I pinged `hostB-10.9.0.6` and in the other host i repeated the same steps but reversing the the pinging hosts:


- Host `hostA-10.9.0.5` pinged `hostB-10.9.0.6`

    ![alt text](<Screenshot 2024-02-29 at 11.03.07 PM.png>)

- Host `hostB-10.9.0.6` pinged `hostA-10.9.0.5`


Using Wiresharke, I monitoring the network interface `br-4a7a76baa4b1` for filtered ICMP traffic and the following are the results of that:

![alt text](<Screenshot 2024-02-29 at 11.09.12 PM.png>)