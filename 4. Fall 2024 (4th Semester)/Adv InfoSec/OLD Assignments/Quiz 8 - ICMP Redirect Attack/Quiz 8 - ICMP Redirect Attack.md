# Quiz 8 - ICMP Redirect Attack

<br />

## Lab Setup:

I am using a remote desktop protocol (RDP) application, Parallels Client, to access the GUI of my GCP SEED Labs Ubuntu instance.  After successfully accessing my instance, I opened up the terminal and completed the following commands to make a directory, do a remote download of the lab's zip file, and unzipped the zip file.
```
mkdir Quiz08
curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/ICMP_Redirect/Labsetup.zip
unzip Labsetup.zip
cd Labsetup
```

![Screenshot 2023-11-02 at 3 01 07 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/d132f080-ed03-455a-a4a2-dc1e97fc9e7b)

<br />


As a process for starting a new class assignment, a few things I like to do is some simple Docker container administration to stop and remove any current docker containers and remove any docker images using the following commands:

  - Bulk Stop Docker Containers: `sudo docker stop $(sudo docker ps -a -q)`
  
  - Bulk Remove Docker Containers: `sudo docker rm $(sudo docker ps -a -q)`
  
  - Bulk Remove Docker Images: `sudo docker rmi $(sudo docker images -q)`

![Screenshot 2023-11-02 at 3 18 37 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/46818b2a-b15a-4b2a-a92d-7de56e5347fc)

<br />


Start building and running the docker containers in the `docker-compose.yml` file:

  - Build the docker containers:  `sudo docker-compose build`
  - Start and run the docker containers:  `sudo docker-compose up`

![Screenshot 2023-11-02 at 3 50 46 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/374604eb-eb14-4f01-9670-1d2e20a6c7b0)

<br />

| Host                            | Host Name     | IP (inet)     | MAC Address (ether)
| ---                            | ---           | ---           | ---
| malicious-router-10.9.0.111    | M-10.9.0.105  | 10.9.0.105    | 02:42:0a:09:00:69
| victim-10.9.0.5                      | A-10.9.0.5    | 10.9.0.5      | 02:42:0a:09:00:05
| host-192.168.60.6            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06
| host-192.168.60.6            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06
| host-192.168.60.6            | B-10.9.0.6    | 10.9.0.6      | 02:42:0a:09:00:06


| Host                          | Host Name       | IP (inet)     | MAC Address (ether)
| ---                           | ---             | ---           | ---
|  victim-10.9.0.5              | ---             | 10.9.0.5      | ---
|  host-192.168.60.6            | ---             | 192.168.60.6  | ---
| malicious-router-10.9.0.111   | ---             | 10.9.0.111    | ---
| host-192.168.60.5             | ---             | 192.168.60.5  | ---
| attacker-10.9.0.105,          | ---             | 10.9.0.105    | ---
| router                        | ---             | ---           | ---




Get the docker network layout using the following command, `sudo docker network ls`

![Screenshot 2023-11-02 at 3 54 08 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/04ecbf3a-d3cd-4a06-89dc-b684d7125f00)


<br />


