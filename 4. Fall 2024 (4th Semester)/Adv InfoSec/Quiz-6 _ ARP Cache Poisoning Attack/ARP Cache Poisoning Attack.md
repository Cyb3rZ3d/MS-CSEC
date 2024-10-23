Ruben Valdez <br /> 
CSEC 5327 | Advanced InfoSec  <br /> 
Prof. Izzat Alsmadi  <br /> 
Tuesday’s@ 4pm  <br /> 

***Quiz 06 - ARP Poisoning Attack***



***Ruben Valdez <br /> Advanced Info Sec | CSEC 5327 | Tuesday’s@ 4pm  <br /> Prof. Izzat Alsmadi***

 ***Quiz 07 - ARP Poisoning Attack***
=======================
<br />
<br />

***Lab and Container Setup***
=======================
<br />

For this lab I'll be using the previously created GCP instance named `seed-lab`.

Using my local host machines terminal, I SSH'ed in to the GCP instance `seed-lab`

The following commands were used to change the user to `RValdez`, navigate to the appropriate directory and create a new directory named `Quiz07`:

```
sudo su - RValdez

cd Documents

mkdir Quiz07
```

Uploaded the `ARP Cache Poisoning Attack Lab` zip file to the instance using the following command:

```
sudo curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/ARP_Attack/Labsetup.zip
```

After downloading the lab setup to the instance, unzip the contents and change the directory into the Labsetup folder:

```
unzip Labsetup.zip

cd Labsetup
```


<br />

***Container Setup*** 
---------------------
<br />

Prior to start of this lab using the prescribed lab docker container, we must first complete the following commands to ensure all prior containers have been stopped and delete, and also ensuring the images have been deleted:

- Bulk Stop Docker Containers:  `sudo docker stop $(sudo docker ps -a -q)`

- Bulk Remove/Delete Docker Containers that have been stopped:  `sudo docker rm $(sudo docker ps -a -q)`

- Bulk remove Docker images from your system:   `sudo docker rm $(sudo docker ps -a -q)`


Now that we have completed some docker maintenance we can build and start the current labs docker containers:

```
sudo docker-compose build

sudo docker-compose up
```

<br />

You can now see the available machines names for the lab:

| Host              | Host Name     | IP
| ---               | ---           | ---
| Host M (Attacker) | M-10.9.0.105  | 10.9.0.105
| Host A            | A-10.9.0.5    | 10.9.0.5
| Host B            | B-10.9.0.6    | 10.9.0.6


<br />

![Alt text](<Screenshot 2023-10-16 at 6.36.55 PM.png>)

<br />

Also, just something that may be needed, I ran the following commands to gather the docker network information:

- Listing out the docker network

    `sudo docker network ls`

- If unable identify the network, run the following command to immediately list the network ID and Name
    
    `docker inspect -f '{{.NetworkSettings.Networks}}{{"\n"}}' M-10.9.0.105`

    ![Alt text](<Screenshot 2023-10-16 at 9.29.36 PM.png>)
<br />

In terminal, open 3 additional tabs and repeat the steps taken to SSH into the GCP instance. After getting into the instance in each terminal, change the directory to Quiz07 using the command `cd Documents/Quiz07`. 

For each terminal run the following docker commands to access each machine separately. Subsequently, run the `ifconfig` to get the network information to identify the MAC address.

- Terminal 1:   
    `sudo docker exec -it M-10.9.0.105 bash`

    ![Alt text](<Screenshot 2023-10-16 at 8.26.14 PM.png>)

- Terminal 2:   
    `sudo docker exec -it A-10.9.0.5 bash`

    ![Alt text](<Screenshot 2023-10-16 at 8.29.55 PM.png>)

- Terminal 3:   
    `sudo docker exec -it B-10.9.0.6 bash`

    ![Alt text](<Screenshot 2023-10-16 at 8.30.45 PM.png>)

<br />
<br />

**Confirmed the following machine IPs and Mac addresses:**

| Host              | Host Name     | IP (inet)     | MAC Address (ether)
| ---               | ---           | ---           | ---
| Host-M (Attacker) | M-10.9.0.105  | 10.9.0.105    | 02:42:0a:09:00:69
| Host-A            | A-10.9.0.5    | 10.9.0.5      | 02:42:0a:09:00:05
| Host-B            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06

<br />
<br />

***Our lab setup is now complete.  We can now proceed to Task 1***

<br />
<br />

***Task 1 - ARP Cache Poisoning***
=======================
<br />

On `Host-M` change to the `seed` directory using the following commang `cd /home/seed`.

| Host              | Host Name     | IP (inet)     | MAC Address (ether)
| ---               | ---           | ---           | ---
| Host-M (Attacker) | M-10.9.0.105  | 10.9.0.105    | 02:42:0a:09:00:69
| Host-A            | A-10.9.0.5    | 10.9.0.5      | 02:42:0a:09:00:05
| Host-B            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06

<br />

## Task 1.A - Using ARP Request
<br />

Perform the following tasks on each host:

- ***Host-M***
    
    - Using nano, create a python file named `M_ARP_Request.py`
    
        ![Alt text](<Screenshot 2023-10-17 at 11.14.34 AM.png>)
    
    - Change the file to an executable using the commande `chmod a+x M_ARP_Request.py`
        
    - execute the program 
    
        ![Alt text](<Screenshot 2023-10-17 at 11.17.14 AM.png>)

- ***Host-A***
    - run the `arp -n` command to view the ARP table
        
        ![Alt text](<Screenshot 2023-10-17 at 11.17.14 AM.png>)

<br />

In the terminal for `Host M`, start the attack by executing the `M_ARP_Request.py` program.

In the terminal for`Host-A`, run the `arp -n` command to access the the ARP table.  Here you can visibly see the IP for `Host-B` but the MAC address doesn't match. The MAC address for `Host-B` (02:42:0a:09:00:06) has been spoofed with the MAC address for `Host-M` (02:42:0a:09:00:69)


<br />
<br />

## Task 1.B - Using ARP reply
<br />

| Host              | Host Name     | IP (inet)     | MAC Address (ether)
| ---               | ---           | ---           | ---
| Host-M (Attacker) | M-10.9.0.105  | 10.9.0.105    | 02:42:0a:09:00:69
| Host-A            | A-10.9.0.5    | 10.9.0.5      | 02:42:0a:09:00:05
| Host-B            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06


- ***Host-M***
    
    - Using nano, create a python file named `M_ARP_Request.py`
    
    - Change the file to an executable using the commande `chmod a+x M_ARP_Request.py`
        
    - execute the program 

To refresh the ARP cache i used `arping` on each respective host:

```
Ping ARP:           arping -c 1 -I <interface_name> <ip_address>

View ARP table:     arp -n

Host-A:     arping -c 1 -I eth0 10.9.0.6
Host-B:     arping -c 1 -I eth0 10.9.0.5

```

Task1.A
![Alt text](<Screenshot 2023-10-17 at 5.30.04 PM.png>)
![Alt text](<Screenshot 2023-10-17 at 5.30.12 PM.png>)


Task 1.B
![Alt text](<Screenshot 2023-10-17 at 5.24.22 PM.png>)
![Alt text](<Screenshot 2023-10-17 at 5.24.41 PM.png>)
![Alt text](<Screenshot 2023-10-17 at 5.25.03 PM.png>)

<br />
<br />

## Task 1.C - Using ARP gratuitous message

<br />

- Created the ARP gratuitous message python program.
- Make the file executable using the `chmod a+x <filename>` command.
- On Host M, execute the `task1c.py` program
- On Host A, check the ARP table
- On Host B, check the ARP table

![Screenshot 2023-10-22 at 5 31 45 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/0efa794d-f222-487f-ab63-a0622e3ed044)

![Screenshot 2023-10-22 at 5 32 05 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/7c5a2f62-788b-47be-a48f-408074fdccfd)

![Screenshot 2023-10-22 at 5 32 35 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/8767d44a-6af9-4c70-94f6-78f62f3c661b)

![Screenshot 2023-10-22 at 5 33 11 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/efd90c4c-989b-4194-9a75-5c2363405fb1)


<br />
<br />


***Task 2 - MITM Attack on Telnet using ARP Cache Poisoning***
=======================
<br />


***Step 1: Launch the ARP cache poisoning***
<br />

Launched a custom ARP cache poisoning attack to both Host A and Host B machines from the attacker Host M machine.

![Alt text](<Screenshot 2023-10-24 at 8.23.21 PM.png>)

<br />



***Step 2: Testing***
<br />

- Turn OFF IP forwarding
- Executing the the python program `task2_ARPcachePoisoningAttack.py`.
- On Host A, ping Host B.
- On Host B, ping Host A.

![Alt text](<Screenshot 2023-10-24 at 2.42.22 PM.png>)

Wireshare results indicate there were dropped packets (no response found).

![Alt text](<Screenshot 2023-10-24 at 2.58.06 PM.png>)

<br />


***Step 3: Turn on IP forwarding***
<br />

- Turn ON IP forwarding
- Executing the the python program `task2_ARPcachePoisoningAttack.py`.
- On Host A, ping Host B.
- On Host B, ping Host A.

![Alt text](<Screenshot 2023-10-24 at 5.04.44 PM.png>)

![Alt text](<Screenshot 2023-10-24 at 5.04.49 PM.png>)

![Alt text](<Screenshot 2023-10-24 at 5.06.02 PM.png>)

![Alt text](<Screenshot 2023-10-24 at 5.05.47 PM.png>)

Looking at the ping in between both host's, it doesn't appear packets were lost, but reviewing Wireshark, there are blocks of request/reply packets showing "no response".  This also indicates there were packets lost.   


<br />

***Step 4: Launch the MITM attack***
<br />

- on Host M, keeping the IP forwarding on from "Step 3"
- on Host A, telnet to Host B
- On Host B, telnet to Host A
- Turn OFF IP forwarding after successfully gaining access to each host from telnet.
- I ran a few commmands on Host A but then the systems would freez and then would close

**NOTE - At this point I wouldn't know what else to do as after completing the last step, the system would freeze then close.  This happened every time I would get to this point in Step 4.   

![Alt text](<Screenshot 2023-10-24 at 9.08.00 PM.png>)

After the system crashed and rebooting the system to start again, I would receive this message:

![Alt text](<Screenshot 2023-10-24 at 8.18.25 PM.png>)


<br />
<br />


# Summary

Overall, this lab was interesting attempting to complete the ARP Cache Poisoning and the MITM attack using the ARP Cache Poisoning Attack simultaneiously. I felt confident completing the assignment up till Task 2 on step 4. Not sure if the issue was my code as to why my system continued to crash at Step 4, but I just couldn't no figure it out much after that.   






