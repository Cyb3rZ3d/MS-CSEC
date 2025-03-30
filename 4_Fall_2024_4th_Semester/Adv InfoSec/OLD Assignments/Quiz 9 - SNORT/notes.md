# Lab Pre-Requisite

Reviewing the assignment, I decided I would be testing Snort using Damn Vulnerable Web Application (DVWA). Not sure how else I could have used DVWA without using Docker.  The following are the steps I took to build the DVWA using docker-compose:

Using my GCP Ubuntu instance I created a few directories:

    mkdir Quiz-9

    mkdir DVWA-docker

After creating the directories needed I could now build my `docker-compose.yml` file using the following command `sudo nano docker-compose.yml`:

![Alt text](<Screenshot 2023-11-29 at 2.20.55 PM.png>)

![Alt text](<Screenshot 2023-11-29 at 2.19.57 PM.png>)

Start and run the DVWA, I ran the `sudo docker-compose up -d` command.

<br />
<br />
<br />
<br />

# Step 1 - Install and Configure Snort

## Install Snort

Installed Snort using the command `sudo apt-get install snort -y`

Simultaneously working between two terminals during the Snort Install/Configuration:

1. I ran the command `/sbin/route -n` to determain what interfaces I should use.
2. I entered the following interfaces `ens4` and `docker0` to be monitored. 

    ![Alt text](<Screenshot 2023-11-27 at 2.08.29 PM.png>)

Used the `ip addr` to record and enter the following IP address and CIDR into the next field.

![Alt text](<Screenshot 2023-11-29 at 2.42.29 PM.png>)

![Alt text](<Screenshot 2023-11-27 at 2.07.22 PM.png>)


## Configure Snort

After the install, I tested the configuration by running the following command `sudo snort -T -c /etc/snort/snort.conf`

![Alt text](<Screenshot 2023-11-29 at 2.54.18 PM.png>)


Moving on, I also needed to check for deprecated rules.  I cycled this one command, `sudo snort -c /etc/snort/snort.conf`, multiple times till I didn't get any further deprecated rules.

Below is a list of deprecated rules I commented out from the specified rule set. The following were key steps I completed to comment out the deprecated rules:

- Reviewed the output and searched for the keyword `deprecated` 
- Using nano, I would do a line search to comment the rule out from the `*.rules` file.  

Command used to modify the rules `sudo nano <rule>.rules`

Deprecated Rules:
```
WARNING: /etc/snort/rules/chat.rules(33) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/dos.rules(42) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/netbios.rules(140) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/netbios.rules(141) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/netbios.rules(142) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/netbios.rules(165) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/netbios.rules(166) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/smtp.rules(62) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/sql.rules(69) threshold (in rule) is deprecated; use detection_filter instead.
WARNING: /etc/snort/rules/sql.rules(73) threshold (in rule) is deprecated; use detection_filter instead.
```

<br />
<br />
<br />
<br />

# Step 2

sudo snort -i <enter the network interface> -q -A console -c /etc/snort/snort.conf