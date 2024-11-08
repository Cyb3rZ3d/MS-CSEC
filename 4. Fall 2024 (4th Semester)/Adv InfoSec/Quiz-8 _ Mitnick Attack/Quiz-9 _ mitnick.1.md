

# Lab Setup

1. Open three terminals and remote into each container using the following commands:

    - `seed-attacker`

        sudo docker exec -it seed-attacker /bin/bash

        ![alt text](<Screenshot 2024-11-07 at 9.08.01 PM.png>)

    - `x-terminal`

        sudo docker exec -it x-terminal-10.9.0.5 /bin/bash

        ![alt text](<Screenshot 2024-11-07 at 9.06.53 PM.png>)

    - `trusted-server`

        sudo docker exec -it trusted-server-10.9.0.6 /bin/bash

        ![alt text](<Screenshot 2024-11-07 at 9.03.55 PM.png>)

<br>

2. Running `ifconfig` for each terminal to gather the network information for this table:

    Network Table:
    ---
    | Docker network    | Host Name                 | IP (inet)     | MAC Address (ether)
    | ---               | ---                       | ---           | ---
    | Network           | net-10.9.0.0              | 10.9.0.0      | ---
    | x-terminal        | x-terminal-10.9.0.5       | 10.9.0.5      | 02:42:0a:09:00:05
    | trusted-server    | trusted-server-10.9.0.6   | 10.9.0.6      | 02:42:0a:09:00:06
    | seed-attacker     | seed-attacker             | 10.9.0.1      | 02:42:27:62:a3:80
    ---

<br><br>

# Task 1

1. On the `x-terminal` I added an ARP entry for the `truster-server` with a fake MAC address to simulate the flooding effect.  This ensures the `x-terminal` has the MAC address cached as it won't receive a response when the `trusted-server` is taked offline.

    - To run this I ran the following commands:

            arp -s 10.9.0.6 aa:bb:cc:dd:ee:ff

            ping -c 1 10.9.0.6 > log.txt

            cat log.txt

        ![alt text](<Screenshot 2024-11-07 at 9.14.12 PM.png>)

    - We can clearly see after printing the ping result's, there was 100% packet loss.  Using wireshark to visibly see the results of the ping, we can see the fake MAC address was successfully transmitted.

        ![alt text](<Screenshot 2024-11-07 at 9.18.16 PM.png>)


<br><br>

# Task 2: 

1. Confirmed the `seed-attacker` in the docker-compose.yml file is set to host mode and privilege mode.
    
    ![alt text](<Screenshot 2024-11-07 at 9.41.23 PM.png>)


## Task 2.1

***Step 1: Spoof a SYN packet***

This step sends a SYN packet from the Trusted Server’s IP to X-Terminal to start the TCP handshake.

1. Python code defining the IP's and ports for the connections:

    Created the python code using nano:

        nano task_2.1.py

    ![alt text](<Screenshot 2024-11-07 at 10.15.55 PM.png>)

2. Commands ran to create the code, change the permissions, and executing the script:

        nano task_2.1.py

        chmod a+x task_2.1.py

        ./task_2.1.py

    After executing the script, outputing the a packet was sent spoofing a SYN packet from the `trusted-server` to the `x-terminal`.

    ![alt text](<Screenshot 2024-11-07 at 10.16.21 PM.png>)

3. Using Wireshark, I was able to sniff the traffic.  Confirming the spoofed packes.

    ![alt text](<Screenshot 2024-11-07 at 10.17.13 PM.png>)

<br>

***Step 2: Respond to the SYN+ACK packet***

Building on top of the existing code but with the note for `Step 2` and saving the new code as `task_2.1.2.py`.

![alt text](<Screenshot 2024-11-07 at 10.43.45 PM.png>)

![alt text](<Screenshot 2024-11-07 at 10.43.03 PM.png>)

![alt text](<Screenshot 2024-11-07 at 10.42.14 PM.png>)

<br>

***Step 3: Spoof the rsh data packet***

Building on top of the existing code but with the note for `Step 3` and saving the new code as `task_2.1.3.py`.

![alt text](<Screenshot 2024-11-07 at 11.45.26 PM.png>)

![alt text](<Screenshot 2024-11-07 at 11.45.53 PM.png>)

I am not sure if this is complete step 3 correctly.  Taking the seq # from step 2 and applying it in the step 3 code doesn't appear to be fully working.   

![alt text](<Screenshot 2024-11-07 at 11.48.24 PM.png>)


## Task 2.2: Spoof the Second TCP Connection

Building on top of the existing code but with the note for `Task 2.2` and saving the new code as `task_2.2.py`.

![alt text](<Screenshot 2024-11-07 at 11.57.52 PM.png>)

![alt text](<Screenshot 2024-11-07 at 11.56.03 PM.png>)

![alt text](<Screenshot 2024-11-07 at 11.58.27 PM.png>)

# Task 3: Set Up a Backdoor

I got lost at this point trying to find the seq number.   I attempted to follow along packets but I just kept getting lost with this task.

Building on top of the existing code but with the note for `Task 3` and saving the new code as `task_3.py`.



# Summary
Over all this lab was difficult for me.  I attempted to follow along the instructions and used a few resouces suck as youtube and the attached samples.   I did have trouble understanding the lab.  It was for sure one of the more challenging labs we have completed this semester.   