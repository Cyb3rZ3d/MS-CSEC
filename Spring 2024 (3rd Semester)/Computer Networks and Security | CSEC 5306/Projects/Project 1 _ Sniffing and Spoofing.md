***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Course Project - Mileston 1 <br>
Due: Feb. 15, 2024 <br>

---

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

#### Troubleshooting issues with Wireshark

I was unable to locate a way to select the appropriate network capture. Troubleshooting the issue, I decided to just reinstall and reconfigure Wireshark. The following is derived using the history  command to list the commands used. Here you'll see the commands used to re-install, reconfigure, adding the user to the Wireshark group, and rebooting the GCP Ubuntu instance. After running the commands I was now able to successfully open Wireshark and see the available network captures I needed to complete the remainder of the task.

![alt text](<Screenshot 2024-02-19 at 10.02.32 PM.png>)

<br>

After rebuilding Wireshark, I was able to successfully run the `sniffer_only_icmp.py` script and then ping `www.google.com`.  Observing the network traffic using a ICMP filter. 

![alt text](<Screenshot 2024-02-20 at 9.29.36 AM.png>)

![alt text](<Screenshot 2024-02-20 at 9.30.00 AM.png>)

![alt text](<Screenshot 2024-02-20 at 9.41.38 AM.png>)

<br>

### Capture any TCP packet that comes from a particular IP and with a destination port number 23.

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

### Capture packets comes from or to go to a particular subnet.

Peformed the command `ip addr show` to gather the Kali VM network subnet.

![alt text](<Screenshot 2024-02-20 at 1.20.05 PM.png>)

