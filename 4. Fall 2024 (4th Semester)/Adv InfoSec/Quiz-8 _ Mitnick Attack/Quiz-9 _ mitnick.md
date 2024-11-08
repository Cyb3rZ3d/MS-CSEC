Ruben Valdez <br> 
CSEC 5327 | Advanced InfoSec  <br> 
Prof. Izzat Alsmadi  <br> 
Tuesday’s@ 7pm  <br> 

# ***Quiz 8 - Mitnick Attack***

<br><br>



https://github.com/Aleem20/Kevin-Mitnick-Attack


## Lab Setup

1. I create a new folder named `MitnickAttack_Quiz-8`, downloaded the `Labsetup.zip` folder, unzipped the .zip folder, and changed directory into the the unziped `Labsetup` folder.

        mkdir MitnickAttack_Quiz-8

        curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/Mitnick_Attack/Labsetup.zip
        
        unzip Labsetup.zip
        
        cd Labsetup

    ![alt text](<Screenshot 2024-11-06 at 1.41.30 PM.png>)


2. Completed Docker maintenance to shutdown any prior docker containers

        sudo docker-compose ps
        sudo docker-compose down

    ![alt text](<Screenshot 2024-11-06 at 2.04.50 PM.png>)

    
    Examined all Docker networks BEFORE starting and running any new containers:

        sudo docker network ls

    ![alt text](<Screenshot 2024-11-06 at 2.08.33 PM.png>)


3. Time to build, create, and start the docker containers using the following commands:

        sudo docker-compose build
        sudo docker-compose up

    After running the following command's I get an error after the command `sudo docker-compose up`:

    ![alt text](<Screenshot 2024-11-07 at 9.05.06 AM.png>)


    Pruned all unused docker resources.  Doing this does the following:

        docker system prune -a --volumes

    - all stopped containers
    - all networks not used by at least one container
    - all anonymous volumes not used by at least one container
    - all images without at least one container associated to them
    - all build cache

    ![alt text](<Screenshot 2024-11-07 at 9.30.39 AM.png>)


    Duplicated steps to build and start the lab docker containers:

        sudo docker-compose build
        sudo docker-compose up


    No error's to report that prevented the build and starting the lab containers

    ![alt text](<Screenshot 2024-11-07 at 9.43.53 AM.png>)


    In another terminal, I verified and confirmed the running containers and listed the docker network:

        sudo docker ps

        sudo docker network ls

    ![alt text](<Screenshot 2024-11-07 at 9.50.09 AM.png>)


## Task 1: Simulated SYN flooding

In this task we take steps to simulate SYN flooding.  In order to complete this task we first need to ping, verify the ARP cache, add a permanent entry to the ARP cache on the `x-terminal` using the `trusted-server`'s IP and MAC address.

1. Using three separate terminals, remoted into every docker container using the following command:

        sudo docker exec -it seed-attacker /bin/bash

        sudo docker exec -it x-terminal-10.9.0.5 /bin/bash

        sudo docker exec -it trusted-server-10.9.0.6 /bin/bash

    For each system, I ran `ifconfig` to verify and confirm each container's IP address:

    ![alt text](<Screenshot 2024-11-07 at 10.10.55 AM.png>)

    ![alt text](<Screenshot 2024-11-07 at 10.11.22 AM.png>)

    ![alt text](<Screenshot 2024-11-07 at 10.11.39 AM.png>)


    Network Table:
    ---
    | Docker network    | Host Name                 | IP (inet)     | MAC Address (ether)
    | ---               | ---                       | ---           | ---
    | Network           | net-10.9.0.0              | 10.9.0.0      | ---
    | x-terminal        | x-terminal-10.9.0.5       | 10.9.0.5      | 02:42:0a:09:00:05
    | trusted-server    | trusted-server-10.9.0.6   | 10.9.0.6      | 02:42:0a:09:00:06
    | seed-attacker     | seed-attacker             | 10.9.0.1      | 02:42:27:62:a3:80
    ---

<br>

2. Ping'ed the `trusted-server` from the `x-terminal` container printing the result's to a `log.txt` file.  After pinging the `trusted-server`, I printed the results using `cat`.

        ping 10.9.0.6 > log.txt

        cat log.txt

    ![alt text](<Screenshot 2024-11-07 at 12.32.29 PM.png>)

    The following steps are commands done to the following terminals `x-terminal`, `trusted-terminal`, and a new terminal on the host. These commands do the following:    

    1. `x-terminal`

        Ping the Trusted Server from X-Terminal
                
            ping -c 1 10.9.0.6 > log.txt
        
        Ping the Trusted Server from X-Terminal, 
        
            arp -a

        Add a Permanent Entry to the ARP Cache

            arp -s 10.9.0.6 02:42:0a:09:00:06

        ![alt text](<Screenshot 2024-11-07 at 1.44.05 PM.png>)

    2. `new terminal`
        
        Stopped the `trusted-server` container

            sudo docker stop trusted-server-10.9.0.6

        ![alt text](<Screenshot 2024-11-07 at 1.41.28 PM.png>)
    
    3. `x-terminal`

        Verified the `trusted-server` is down

            ping -c 1 10.9.0.6 > log.txt

            cat log.txt

        ![alt text](<Screenshot 2024-11-07 at 1.42.21 PM.png>)


## Task 2: Spoof TCP Connections and rsh Sessions

1. Opening `Wireshark`, I wasn't seeing any network traffic running on the network interface so i 

        sudo systemctl restart NetworkManager

        sudo dpkg-reconfigure wireshark-common
        sudo adduser $USER wireshark
        sudo wireshark
        sudo reboot

2. 









### Task 2.1: Spoof the First TCP Connection



### Task 2.2: Spoof the Second TCP Connection



## Task 3: Set Up a Backdoor



# Summary


