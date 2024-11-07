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


3. Pruned all unused docker resources.  Doing this does the following:

    - all stopped containers
    - all networks not used by at least one container
    - all anonymous volumes not used by at least one container
    - all images without at least one container associated to them
    - all build cache


            docker system prune -a --volumes





## Task 1: Simulated SYN flooding



## Task 2: Spoof TCP Connections and rsh Sessions



### Task 2.1: Spoof the First TCP Connection



### Task 2.2: Spoof the Second TCP Connection



## Task 3: Set Up a Backdoor



# Summary


