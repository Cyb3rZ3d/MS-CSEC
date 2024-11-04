# Quiz 8 - ICMP Redirect Attack

<br />

# Lab Setup:

I am using a remote desktop protocol (RDP) application, Parallels Client, to access the GUI of my GCP SEED Labs Ubuntu instance.  After successfully accessing my instance, I opened up the terminal and completed the following commands to make a directory, do a remote download of the lab's zip file, and unzipped the zip file.

```
mkdir Quiz08
curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/ICMP_Redirect/Labsetup.zip
unzip Labsetup.zip
cd Labsetup
```

![alt text](<Screenshot 2024-11-02 at 7.35.06 PM.png>)

![alt text](<Screenshot 2024-11-02 at 7.35.29 PM.png>)

---

As a process for starting a new class assignment, a few things I like to do is some simple Docker container administration to stop and remove any current docker containers and remove any docker images using the following commands:

  - Bulk Stop Docker Containers: 
    
    `sudo docker stop $(sudo docker ps -a -q)`
  
  - Bulk Remove Docker Containers: 
  
    `sudo docker rm $(sudo docker ps -a -q)`
  
  - Bulk Remove Docker Images: 
  
    `sudo docker rmi $(sudo docker images -q)`

---

Start building and running the docker containers in the `docker-compose.yml` file:

  - Build the docker containers:  
  
    `sudo docker-compose build`

  - Start and run the docker containers:  
    
    `sudo docker-compose up`

    ![alt text](<Screenshot 2024-11-02 at 8.51.09 PM.png>)

---

| Host                          | Host Name       | IP (inet)     | MAC Address (ether)
| ---                           | ---             | ---           | ---
| router                        | ---             | 10.9.0.11     | ---
| malicious-router-10.9.0.111   | ---             | 10.9.0.111    | ---
| attacker-10.9.0.105           | ---             | 10.9.0.105    | ---
| victim-10.9.0.5               | ---             | 10.9.0.5      | ---
| host-192.168.60.6             | ---             | 192.168.60.6  | ---
| host-192.168.60.5             | ---             | 192.168.60.5  | ---

---

Get the docker network layout using the following command

`sudo docker network ls`  

![alt text](<Screenshot 2024-11-02 at 9.18.00 PM.png>)


<br><br>


# Task 1: Launching ICMP Redirect Attack

1. Confirmed the countermeasure to prevent ICMP redirect attacks has been disabled and set to `1`.

    ![alt text](<Screenshot 2024-11-02 at 10.20.06 PM.png>)


2. Opened up multiple terminal's to remote into each container using the following commands:

    - List of all the containers:

          sudo docker-compose ps
      
        ![alt text](<Screenshot 2024-11-03 at 2.57.27 PM.png>)

    - Attacker terminal:

          sudo docker exec -it attacker-10.9.0.105 bash

        ![alt text](<Screenshot 2024-11-03 at 2.55.09 PM.png>)

    - Victim Terminal: 
        
          sudo docker exec -it victim-10.9.0.5 bash

        ![alt text](<Screenshot 2024-11-03 at 2.56.12 PM.png>)

    - Malicious-Router terminal:

          sudo docker exec -it malicious-router-10.9.0.111 bash

        ![alt text](<Screenshot 2024-11-03 at 2.57.09 PM.png>)

    - Host-192.168.60.5 terminal:

          sudo docker exec -it host-192.168.60.5 bash

        ![alt text](<Screenshot 2024-11-03 at 2.56.33 PM.png>)

<br>

3. `Attacker Terminal`

    - Modified the python script using the provided skeleton code for the lab

      - Explanation of Parameters:
        - src="192.168.60.11": Source IP of the legitimate router.
        - dst="10.9.0.5": Destination IP (victim’s IP).
        - icmp.gw="10.9.0.111": The IP of the malicious router that will receive rerouted traffic.
        - ip2: Encapsulates the packet the victim initially intended to send.

      ![alt text](<Screenshot 2024-11-03 at 3.07.27 PM.png>)

    - Modified permission of Task01.py using the following command

          chmod a+x Task01.py

    - Execute the script using `./Task01.py`

      ![alt text](<Screenshot 2024-11-03 at 3.16.00 PM.png>)


4. `Victim Terminal` 

  - Pinged to a `log.txt file then cated the the results

    `ping 192.168.60.5 > log.txt`

    ![alt text](<Screenshot 2024-11-03 at 3.37.09 PM.png>)

  - Did a traceroute of the victim machine

    `mtr -n 192.168.60.5`

    ![alt text](<Screenshot 2024-11-03 at 3.13.38 PM.png>)


## Question 1: Can you use ICMP redirect attacks to redirect to a remote machine? Namely, the IP address assigned to icmp.gw is a computer not on the local LAN. Please show your experiment result, and explain your observation.

The only thing I did was change the `icmp.gw` IP address to a system that is not on the local LAN. 

- Attacker terminal

  ![alt text](<Screenshot 2024-11-03 at 3.53.46 PM.png>)

- Victim terminal

  ![alt text](<Screenshot 2024-11-03 at 3.59.40 PM.png>)

  ![alt text](<Screenshot 2024-11-03 at 3.52.28 PM.png>)

After executing the script on the Attacker container, and checking the cache on the Victim container, I found that I'm unable to run a ICMP redirect attack to a computer not on the local LAN.  

## Question 2: Can you use ICMP redirect attacks to redirect to a non-existing machine on the same network? Namely, the IP address assigned to icmp.gw is a local computer that is either offline or non-existing. Please show your experiment result, and explain your observation.

- Attacker:

  Modified the script to change the `icmp.gw` to IP `10.9.0.200`.

  ![alt text](<Screenshot 2024-11-03 at 4.19.57 PM.png>)

  ![alt text](<Screenshot 2024-11-03 at 4.20.37 PM.png>)

- Victim:

  Ran the following commands to flush the cache, show the cache, run a ping and the output the results to a .txt file, then ran a traceroute to view packets sent and received between two IPs:

      ip route flush cache
      ip route show cache
      ping 192.168.60.5 > log.txt  
      mtr -n 192.168.60.5

  ![alt text](<Screenshot 2024-11-03 at 4.32.47 PM.png>)

  ![alt text](<Screenshot 2024-11-03 at 4.29.31 PM.png>)

I don't understand how packet's were 100% received and not dropped.  Theoretically these should have been dropped since the IP `10.9.0.200` device is non-existant.  


## Question 3: If you look at the docker-compose.yml file, you will find the following entries for the malicious router container. What are the purposes of these entries? Please change their value to 1, and launch the attack again. Please describe and explain your observation.


- See highlighted setting value's 

  ![alt text](<Screenshot 2024-11-03 at 4.37.38 PM.png>)

- Changed all highlighted setting's to reflect value's from 0 to 1 

  ![alt text](<Screenshot 2024-11-03 at 4.38.18 PM.png>)

- After restarting the docker containers from refreshing the .yml file, I lost all prior python scripts I created prior to this script.  

Attacker:

  ![alt text](<Screenshot 2024-11-03 at 4.50.52 PM.png>)

  ![alt text](<Screenshot 2024-11-03 at 4.56.07 PM.png>)

Victim:
  
  ![alt text](<Screenshot 2024-11-03 at 4.57.13 PM.png>)

  ![alt text](<Screenshot 2024-11-03 at 4.54.50 PM.png>)

Same as with Q1 and Q2, my result's are the same.  I am unable to figure the issue out  But even modifying the .yml config file, it doesn't appear I am getting any different results.  


# Task 2: Launching the MITM Attack

1. Establishing `netcat` connection and tested the connection by entering `Hi, am I in?`

  - Target: `host-192.168.60.5`

      ![alt text](<Screenshot 2024-11-03 at 5.24.09 PM.png>)

  - Victim: `victim-10.9.0.5`

      ![alt text](<Screenshot 2024-11-03 at 5.26.09 PM.png>)

2. Disbled the attacker's `Malicious-Router`

  - Malicious-Router: `malicious-router-10.9.0.111`

      ![alt text](<Screenshot 2024-11-03 at 5.34.29 PM.png>)


3. Executing the MiTM script and verifiying connections

  - Attacker:

    Created a MiTM.py:

      ![alt text](<Screenshot 2024-11-03 at 5.55.51 PM.png>)

    Executed MiTM script to capture traffic between the Victim and the Host machines.

4.  MiTM attack and confirmation.

  - Victim: 

      Entered a text `Hello, my name is Ruben`

      ![alt text](<Screenshot 2024-11-03 at 6.14.49 PM.png>)

  - host-192.168.60.5:

      Confirmed the message was received

      ![alt text](<Screenshot 2024-11-03 at 6.11.27 PM.png>)

  - Attacker:

    We can see the message was intercepted from the communications between the victem and host machines.

    ![alt text](<Screenshot 2024-11-03 at 6.13.57 PM.png>)


5. 

![alt text](<Screenshot 2024-11-03 at 6.50.01 PM.png>)



