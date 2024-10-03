Ruben Valdez <br>
CSEC 5327 _ Advanced InfoSec <br>
Prof. Dr. Alsmadi <br>
Quiz-4 _ Morris Worm <br>
Due: Oct. 4th, 2024 <br>
===

<br>

# Labsetup

- SSH into the GCP instance using terminal

    `ssh -i adv-infosec ruben.valdez0@35.202.142.237`   

    <br>

- Created directory named `MorrisWorm_Quiz-4`

    ![alt text](<Screenshot 2024-10-02 at 8.10.26 AM.png>)

    <br>

- Downloaded the `Labsetup.zip` file

    `sudo curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/Morris_Worm/Labsetup.zip`

    ![alt text](<Screenshot 2024-10-02 at 8.26.13 AM.png>)  
    
    ![alt text](<Screenshot 2024-10-02 at 8.26.47 AM.png>)  
    
    <br>

# Task 1: Get Familiar with the Lab Setup
***NOTE: Task 1-5 are using `internet-nano`***  <br>


- Let's build and start the `internet-nano` docker container's using `docker-compose`.

    - Build the docker containers

        ![alt text](<Screenshot 2024-10-02 at 12.51.31 PM.png>)

        ![alt text](<Screenshot 2024-10-02 at 12.51.51 PM.png>)

    - Start and run the docker container's

        ![alt text](<Screenshot 2024-10-02 at 12.58.03 PM.png>)

        ![alt text](<Screenshot 2024-10-02 at 12.58.32 PM.png>)

- After the docker containers have been built and started let's take a look at the network diagram and check out the emulator by navigating to the map `http://localhost:8080/map.html`.

    ![alt text](<Screenshot 2024-10-02 at 1.08.25 PM.png>)


- Let run a quick test and ping a node.

    - Using docker, I remoted into ID `138a0f40ab31`, IP `10.152.0.75`.

    - Ran the ping command `ping 1.2.3.4` 

    - In the `Filter` box I typed `ICMP and dst 1.2.3.4` of the map

        ![alt text](<Screenshot 2024-10-02 at 1.32.13 PM.png>)

    We can see the ping starting from `10.152.0.75` host, connecting to the `10.152.0.0/24` network hub, and pinging up to 152/router `10.152.0.254/24`.


<br>

# Task 2: Attack the First Target using a `buffer-overflow` vulernability

- Turning off the address randomization. 
    
    - This kernel parameter is global, so once we turn it off from the host machine, all the containers are affected.
    
    `sudo /sbin/sysctl -w kernel.randomize_va_space=0`



<br>

# Task 3: Self Duplication



<br>

# Task 4: Propagation




