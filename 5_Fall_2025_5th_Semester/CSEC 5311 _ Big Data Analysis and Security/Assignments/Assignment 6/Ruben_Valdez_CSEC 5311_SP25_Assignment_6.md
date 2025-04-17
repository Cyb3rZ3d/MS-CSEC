Ruben Valdez <br>
CSEC 5311 | Big Data Analysis and Security <br>
Prof. Hossain, Tamjid <br>
Assignment 6: Hadoop <br>
Due. April 17, 2025 <br><br>


# Lab Setup

I attempted to use the provided Lab PDF instructions to complete the install successfully, but when attempting to complete the assignment, I was encountering a few errors along the way that prevented me from successfully completing the assignment.  Just not as comfortable using `Windows` as much as I am using `Linux`.  In the admin space and programming I predominately use `VScode` and instead of using a virtual machine I decided to try `WSL` to complete this assignment. This decision comes after reviewing an article on `medium.com` installing `WSL` and using `VScode` where I can also clone my `Github` repository.  The following are steps I took to install `WSL` and the `Ubuntu-24.04` distro, and not as much showing what my repo API was or is for security purposes.  

Article used for the assist to complete the steps:  https://medium.com/@farimomoh/installing-ubuntu-on-wsl-and-working-with-vscode-on-windows-f5ab7f286f13

<br>

1. WSL and Ubuntu 24.04 Install

    - Install `wsl`

            wsl --install

            Note:  By default `linux` is installed.


    - Look up linux distros to install

            wsl --list --online

    - Downloading the `Ubuntu-24.04`

            wsl --install -d Ubuntu-24.04

    - List state of any current stopped or running containers

            wsl -l -v

            Note: Noticed by default all disros are in a stopped state.

    - Set `Ubuntu-24.04` as the default WSL distro and started the distro.  After starting the distro I was also presented to create a username and password (see 2nd screenshot)

            wsl --set-default Ubuntu-24.04

            wsl -d Ubuntu-24.04
        
        ![alt text](<Screenshot 2025-04-17 103806.png>)  ![alt text](<Screenshot 2025-04-16 132259.png>)

    - Update and Upgrade your ubuntu distro using `sudo apt update && sudo apt upgrade -y`

    - Make sure to enable `systemd` as it provides support for manating features managing processes and services. As a note, `systemd` was already enabled true on my distro.

            sudo nano /etc/wsl.confi
            
            #Add these lines to your file.
            [boot]
            systemd=true

    - Reboot `Ubuntu`.  ***NOTE:*** DO not run this command in the Ubuntu terminal.  Rather, use Powershell or Commandline.

            wsl --shutdown

<br>

2. VScode

    - Open `Extensions` and install `Remote Developement`

    - I went to my GitHub and created a new repository `WSL_Ubuntu_20.04`

        - Also, while I was in Github, I needed to create and generate a personal access token (PAT) to be able to clone my repository in the ubuntu distro.

    - In the WSL Ubuntu distro, clone using HTTPS with PAT

            git clone https://github.com/Cyb3rZ3d/WSL_Ubuntu_20.04.git

            Note: when promped I used my Github username and pasted my PAT

        ***SUCCESS*** I have access to my repo.

        ![alt text](image-5.png)

<br>

3.  Install and configure Ubuntu for JAVA

    - Installing Java 8 JDK

            sudo apt install openjdk-8-jdk -y

    - Confirm the java install

            java -version

    - Add exceptions to the the `.bachrc` file

            echo "export JAVA_HOME=$(readlink -f /usr/bin/java | sed 's:bin/java::')" >> ~/.bashrc
            echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> ~/.bashrc
            source ~/.bashrc

    - Confirm the config file was updated by opening the file and looking for the exceptions and add the note above the exceptions to note listing them as Java.

            nano ~/.bashrc

    ***NOTE:*** Missed out taking screenshots of majority of all administrative commands to setup this lab because the terminal wouldn't allow me to scroll up as it would stop after scrolling up a bit.  I'm relying on command `history` to show my commands ran.

    ![alt text](image-6.png)

4. Hadoop install

    - Completed the following commands to install Hadoop

            wget https://archive.apache.org/dist/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz
            
            tar -xvzf hadoop-3.0.0.tar.gz
            
            mv hadoop-3.0.0 hadoop
            
            hadoop version

            nano ~/.bashrc
           
            nano ~/hadoop/etc/hadoop/hadoop-env.sh

        ![alt text](image-7.png)

        - Added the `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64` to the bash fiel `/home/rubva/hadoop/etc/hadoop/hadoop-env.sh `
        
            ![alt text](image-8.png)

        - Added and confirmed the Hadoop exceptions were added

            ![alt text](image-9.png)


5. Kaggle CSV download

    - Installed Python3, and created a virtualized environment.

    - pip install kaggle

    - Retrieved Kaggle account API key `kaggle.json`

    - Completed the following commands to place the API key

            mkdir -p ~/.kaggle

            Downloaded the API key from PC to Ubuntu:
            cp /mnt/c/Users/rubva/Downloads/kaggle.json ~/.kaggle/

            chmod 600 ~/.kaggle/kaggle.json

            cd ~/Hadoop-Assignment

            kaggle datasets download -d elemento/nyc-yellow-taxi-trip-data

            sudo apt install unzip

            unzip nyc-yellow-taxi-trip-data.zip yellow_tripdata_2016-03.csv

        ![alt text](image-10.png)  ![alt text](image-11.png)


<br><br><br>

# Task 1: Number of Trips per Hour of Day

1. Created the mapper script; 

- mapper_task_1.py  
        


- reducer_task_1.py




![alt text](image-3.png)


# Task 2: Most Popular Pickup Location (Zone ID or Coordinates)







# Task 3: Average Fare per Passenger Count 
















