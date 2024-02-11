Ruben Valdez <br />
CSEC 5306 | Computer Networks and Security <br />
Prof. Alsmadi <br />
Quiz 1: Crypto Lab -- Secret-Key Encryption

<br />

# Lab Setup

1. Created a GCP Instance to host the SEED Lab environment.

   ![Screenshot 2024-02-05 at 2 34 05 PM](https://github.com/Cyb3rZ3d/MS-CSEC/assets/108482007/dca73ebd-1c18-4e6e-928d-21766d6ff964)

2. Set up the remote desktop environment using `Chrome Remote Desktop`
  - SSH into the GCP instance `csec5306-netsec` and run the following commands:
    - Enable Desktop Expereince:
      ```
      sudo apt-get update
      sudo apt-get install -y xrdp
      sudo apt-get install -y xfce4
      sudo service xrdp restart
      ```

    - `Chrome Remote Desktop` setup:
      - Navigate to https://remotedesktop.google.com/ and complete the steps to "Access my computer".  
      - SSH into the GCP instance. For this example, I'm using Ubuntu, and run the following commands:
        ```
        sudo apt update -y
        sudo apt install --assume-yes wget tasksel
        sudo wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
        sudo apt-get install --assume-yes ./chrome-remote-desktop_current_amd64.deb
        sudo tasksel install ubuntu-desktop
        sudo bash -c 'echo "exec /etc/X11/Xsession /usr/bin/gnome-session" > /etc/chrome-remote-desktop-session'
        sudo systemctl status chrome-remote-desktop@USER
        sudo reboot
        ```
        
     - After the reboot, SSH back into your GCP instance.
     - Navigating between SSH and Google Chrome Remote Desktop windows.
     - In the Chrome Remote Desktop window, on the left sidebar complete the steps to "Set up via SSH"
     - Copy/paste the provided command into the GCP instance SSH window.


3. Open Terminal, change the directory to `Desktop` and create a folder named `Quiz-1_NetSec`.

   ![Screenshot 2024-02-05 at 2 57 45 PM](https://github.com/Cyb3rZ3d/MS-CSEC/assets/108482007/1fef646e-0938-4e90-aded-40f3cee7bb9e)


<br/>
<br/>

# Lab Environment

1. Download the Crypto Lab -- Secret-Key Encryption `Labsetup.zip` file:
   
   `
   sudo curl -o Labsetup.zip https://seedsecuritylabs.org/Labs_20.04/Files/Crypto_Encryption/Labsetup.zip
   `
   
   ![Screenshot 2024-02-05 at 4 02 40 PM](https://github.com/Cyb3rZ3d/MS-CSEC/assets/108482007/d23bcea1-3bc4-49e5-bb7b-cf3b179ae49d)


2. 











