Ruben Valdez 
Advanced Info Sec | CSEC 5327 | Tuesday’s@ 4pm
Prof. Izzat Alsmadi

Assignment | Quiz 5 - Packet Sniffing and Spoofing	



# Docker Commands used in this lab:

- ***Docker Container Administration:***

    Bulk Stop Docker Containers:  `sudo docker stop $(sudo docker ps -a -q)`
    
    Bulk Remove/Delete Docker Containers that have been stopped:  `sudo docker rm $(sudo docker ps -a -q)`
    
    To start build a container:  `sudo docker-compose build`
    
    To start a container:  `sudo docker-compose up`

--------------------------------------------------------------------------------
<br />

- ***Access Docker Containers:***

    To log into a docker container:  `sudo docker exec -it <NAME OF CONTAINER> bash`


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
<br />


# Labsetup:

***Containers:*** 

`seed-attack` &nbsp; `hostA-10.9.0.5` &nbsp; `hostB-10.9.0.6`

<br />


***Container Network Details:***  

- **`seed-attacker`**

  Network Interface details:

  ![DockerNetworkInternface.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12822613/DockerNetworkInternface.pdf)


-  **`hostA-10.9.0.5`**

    ![Screenshot 2023-10-05 at 2.53.37 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12822717/Screenshot.2023-10-05.at.2.53.37.PM.pdf)


-  **`hostB-10.9.0.6`**

    ![Screenshot 2023-10-05 at 3.02.06 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12822790/Screenshot.2023-10-05.at.3.02.06.PM.pdf)


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
<br />


# Task 1

***`seed-attacker`*** 

Using nano, create a python file named `mycode.py` using the following code:

![Screenshot 2023-10-06 at 9.58.59 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12832457/Screenshot.2023-10-06.at.9.58.59.AM.pdf)

<br />

There are three methods to execute the `mycode.py` program:

  1. Using the `python3` command, after receiving the results, change the `mycode.py` file to an executable using the command `chmod a+x mycode.py` followed by running the `ls -l` command to verify the file permissions were updated:

     ![Screenshot 2023-10-06 at 10.17.24 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12832723/Screenshot.2023-10-06.at.10.17.24.AM.pdf)
  
  2. Execute the python program as is `mycode.py` or `./mycode.py`:

     ![Screenshot 2023-10-06 at 1.08.31 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12834253/Screenshot.2023-10-06.at.1.08.31.PM.pdf)
  
  3. Enter the python prompt using `python3` and executeed the provided code:
     ![Screenshot 2023-10-06 at 1.16.53 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12834310/Screenshot.2023-10-06.at.1.16.53.PM.pdf)


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
<br />


# Task 1.1 - Sniffing Packets

Create a new python program using the filename `task_1.1.py`

![Screenshot 2023-10-07 at 11.47.45 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839809/Screenshot.2023-10-07.at.11.47.45.PM.pdf)


--------------------------------------------------------------------------------
<br />


## Task 1.1A - Make the program executable

Use the `chmod a+x task_1.1.py` command to make the python program executable

![Screenshot 2023-10-07 at 11.51.46 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839816/Screenshot.2023-10-07.at.11.51.46.PM.pdf)


--------------------------------------------------------------------------------
<br />


## Task 1.1B - Executing the sniffer

<br />

### Capture only the ICMP packets

Modified the python program `task_1.1.py`

![Screenshot 2023-10-08 at 12.35.00 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839858/Screenshot.2023-10-08.at.12.35.00.AM.pdf)


Start the sniffer on the `seed-attacker` machine using the following commange `./task_1.1.py`.  

![Screenshot 2023-10-08 at 12.20.25 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839843/Screenshot.2023-10-08.at.12.20.25.AM.pdf)


From the `hostA-10.9.0.5` machine, use the `ping 10.9.0.6` command to ping for ICMP packets to the `hostB-10.9.0.6` machine

![Screenshot 2023-10-08 at 12.14.45 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839835/Screenshot.2023-10-08.at.12.14.45.AM.pdf)


Navigate back to the  machine to view the ICMP packets that were pinged

![Screenshot 2023-10-08 at 12.14.13 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839834/Screenshot.2023-10-08.at.12.14.13.AM.pdf)


--------------------------------------------------------------------------------
<br />


### Capture any TCP packet that comes from a particular IP and with a destination port number 23

Modified and updated the `Task_1.1.py` python program code

![Screenshot 2023-10-08 at 12.37.36 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12839861/Screenshot.2023-10-08.at.12.37.36.AM.pdf)

Start the sniffer on the `seed-attacker` machine using the following command `./task_1.1.py`.  

From the`hostA-10.9.0.5` machine use the following `telnet 10.9.0.6` command to start a unsecured remote connection to the `hostB-10.9.0.6` machine.

![Screenshot 2023-10-08 at 12.51.03 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12841334/Screenshot.2023-10-08.at.12.51.03.PM.pdf)

Come back to the `seed-attacker` machine to view the scapy traffic packets after starting a telnet connection between the `hostA-10.9.0.5` and `telnet 10.9.0.6` hosts.

![Screenshot 2023-10-08 at 12.50.33 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12841331/Screenshot.2023-10-08.at.12.50.33.PM.pdf)


--------------------------------------------------------------------------------
<br />

### Capture packets comes from or to go to a particular subnet. You can pick any subnet, such as `10.9.0.0/24` should not pick the subnet that your VM is attached to.


Used the following command to find the labs subnet `sudo docker network inspect net-10.9.0.0`

&emsp; [Docker Networking Basics](https://dockerlabs.collabnix.com/networking/A1-network-basics.html#:~:text=The%20docker%20network%20inspect%20command,networks%20on%20your%20Docker%20host) is the resource used to research steps how to find the docker subneth. 

<br />

Modified the `./task_1.1.py` python program to make adjustments to the filter.

![Screenshot 2023-10-08 at 2.30.34 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12841555/Screenshot.2023-10-08.at.2.30.34.PM.pdf)


Start the sniffer on the `seed-attacker` machine using the following command `./task_1.1.py`.  


From the `hostA-10.9.0.5` machine, ping `10.9.0.6`

![Screenshot 2023-10-08 at 2.47.37 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12841611/Screenshot.2023-10-08.at.2.47.37.PM.pdf)


View the incoming sniffed packets on the `seed-attacker` machine

![Screenshot 2023-10-08 at 2.51.10 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12841616/Screenshot.2023-10-08.at.2.51.10.PM.pdf)


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
<br />


# Task 1.2 - Spoofing ICMP Packets

Created a python program called `Task_1.2.py`

Some things to note, I modified the original python code w/in the lab to add `a.src = '10.9.0.5` since the task was to spoof ICMP between the `hostA-10.9.0.5` and `hostB-10.9.0.6` hosts from the `seed-attacker` machine.

![Screenshot 2023-10-10 at 10.57.45 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12859224/Screenshot.2023-10-10.at.10.57.45.AM.pdf)


From the onset attempting to use Wireshark, I was unable to locate a way to select the appropriate network capture.  Troubleshooting the issue, I decided to just reinstall and reconfigure Wireshark.  The following is derived using the `history ` command to list the commands used.  Here you'll see the commands used to re-install, reconfigure, adding the user to the Wireshark group, and rebooting the GCP Ubuntu instance.  After running the commands I was now able to successfully open Wireshark and see the available network captures I needed to complete the remainder of the task.

    ```
    758  sudo apt-get install wireshark
    759  sudo wireshark
    760  sudo dpkg-reconfigure wireshark-common
    761  sudo adduser $USER wiresheark
    762  sudo adduser $USER wireshark
    763  reboot
    764  sudo reboot
    ```

![Screenshot 2023-10-10 at 8.58.46 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12858047/Screenshot.2023-10-10.at.8.58.46.AM.pdf)


Now we can begin Spoofing ICMP packets:

- Start running Wireshark:

    - Select the netork capture `br-b6b8f465ceb0` (this is the labs network bridge) and enter `host 10.9.0.5` into the filter and then press enter to start the capture.

      ![Screenshot 2023-10-10 at 11.55.42 AM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12859836/Screenshot.2023-10-10.at.11.55.42.AM.pdf)

    - Execute the python program `task_1.2.py` and watch for the packet that will result from running the program and watch the Wireshark screen to confirm the spoofed ping for ICMP packets.  Watching for the request and reply betweeen the `hostA-10.9.0.5` and `hostB-10.9.0.6` hosts.

      ![Screenshot 2023-10-10 at 12.04.47 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12859929/Screenshot.2023-10-10.at.12.04.47.PM.pdf)

      ![Screenshot 2023-10-09 at 11.28.02 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12859700/Screenshot.2023-10-09.at.11.28.02.PM.pdf)
      
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
<br />


# Task 1.3 - Traceroute

Create a new python program named `Task_1.3.py`
    
The code uses the Scapy library to estimate the number of routers (hops) between the current system and a specified destination IP (in this case, '10.9.0.5').

Function jump(ttl):
    Sends an ICMP packet (ping) to the target destination with a specified Time-To-Live (TTL) value.
    If the TTL expires before reaching the destination, the intermediate router sends back an "ICMP Time-to-live exceeded" message. The function then returns the IP address of this router.
    If no response is received, it indicates that the hop didn't reply or the packet was dropped.

Function main():
    Iterates TTL values from 1 to 30, simulating the traceroute process.
    Collects IP addresses of routers that reply during this process.
    At the end, it calculates and prints the number of unique hops and the sum of TTL values used to reach these hops.

When the script is run, the main() function executes, and the code tries to trace the route to '10.9.0.5', reporting on each router it encounters along the way.

![Screenshot 2023-10-10 at 3.38.43 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12861620/Screenshot.2023-10-10.at.3.38.43.PM.pdf)

Change the file to be executable using the command `chmod a+x Task_1.3.py`.

Start the Wireshark capture and run the python program `Task_1.3.py` and view the packet.

- After running the program
  
  ![Screenshot 2023-10-10 at 3.30.48 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12861567/Screenshot.2023-10-10.at.3.30.48.PM.pdf)

- Reveiw the Wireshark details
  
    - ICMP request
    
      ![Screenshot 2023-10-10 at 3.36.31 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12861600/Screenshot.2023-10-10.at.3.36.31.PM.pdf)
    
    - ICMP reply
    
      ![Screenshot 2023-10-10 at 3.32.11 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12861581/Screenshot.2023-10-10.at.3.32.11.PM.pdf)


# Task 1.4: Sniffing and-then Spoofing

Created a new python program `Task_1.4.py`

![Screenshot 2023-10-10 at 5.19.32 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12862234/Screenshot.2023-10-10.at.5.19.32.PM.pdf)


Generate ICMP traffic on `hostA-10.9.0.5` and `hostB-10.9.0.6`

![Screenshot 2023-10-10 at 5.21.13 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12862240/Screenshot.2023-10-10.at.5.21.13.PM.pdf)

Wireshark traffic on network bridge `br-b6b8f465ceb0`

![Screenshot 2023-10-10 at 5.22.03 PM.pdf](https://github.com/Cyb3rZ3d/Class_SEEDLabs/files/12862246/Screenshot.2023-10-10.at.5.22.03.PM.pdf)




# Summary

I encountered several challenges while working through this lab, with the bulk of my difficulties centering around troubleshooting with Wireshark. Tasks 1.1 through 1.4 posed specific challenges, particularly when it came to writing effective Python code. While I invested significant time and thought into constructing each program, I recognize that my beginner skill level necessitated extensive research to help me navigate the process. Perhaps I overcomplicated some aspects, but regardless, I found the insights and knowledge I gained to be invaluable.

Before this lab, I had never used GitHub for building or formatting, so my experience was virtually non-existent. Learning to use, build, and format notes, images, and code in real-time presented a steep learning curve as I progressed through the lab.




