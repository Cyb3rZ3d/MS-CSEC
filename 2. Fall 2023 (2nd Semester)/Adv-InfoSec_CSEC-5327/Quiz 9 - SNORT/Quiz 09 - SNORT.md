

***Ruben Valdez <br /> Advanced Info Sec | CSEC 5327 | Tuesday’s@ 4pm  <br /> Prof. Izzat Alsmadi***

 ***Quiz 09 - SNORT Lab***
=======================
<br />
<br />



# SNORT Lab
<br />

## STEP 1 - Install and Configure SNORT

### SNORT Lab:

Install SNORT

`sudo apt-get install snort -y`

Uninstall SNORT

`sudo apt-get purge --auto-remove snort -y`

---

### SNORT Setup:

1. Follow the `Package Configuration` prompt.  Open another terminal tab and use the following commands to list the IP routing table to determine the network interface and the IP:
   - `/sbin/route -n`  OR  `ip addr`
   -  IP:  10.128.0.0/32
   -   iface: ens4


2. Using the `nano` text editor, I modified the snort.config file, replacing `any` with the GCP external IP.

   Step #1: Set the network variables.  For more information, see README.variables

   ![Screenshot 2023-11-13 at 4 40 49 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/f74157df-699e-4568-8637-a806b0c926a1)


3. Tested the configuration with the command:  `sudo snort -T -c /etc/snort/snort.conf`

   Received a successful configuration message.

   ![Screenshot 2023-11-13 at 4 42 41 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/83456932-4683-4998-a79c-37df81dccf1e)


4. Ran the command `sudo snort -c /etc/snort/snort.conf` to check the SNORT configuration file to look for any files containing a deprecated format.  For each deprecated result, I would access the specific .rules file and apply the `#` at the beginning of the rule to comment the rule out.

   NOTE:  Ran the command after updating every deprecated file until no further rules were deprecated.

   NOTE:  I searched for the line number to make the search more effortless in the .rules file.

   NOTE:  After the 2nd deprecated screenshot, I forgot to take screenshots of the remainder of the deprecated rule updates.

   ***List of Depracated rules I updated:***

   - /etc/snort/rules/chat.rules(33) threshold (in rule) is deprecated; use detection_filter instead.

     <img width="1023" alt="Screenshot 2023-11-09 at 9 20 48 PM" src="https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/85437b6c-64f4-4926-a368-992f9bec6483">
     
   - /etc/snort/rules/dos.rules(42) threshold (in rule) is deprecated; use detection_filter instead.

     ![Screenshot 2023-11-09 at 9 38 53 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/043c3e58-4f66-4640-ba6c-066a1e1f5a7d)

   - /etc/snort/rules/netbios.rules(140) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/netbios.rules(141) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/netbios.rules(142) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/netbios.rules(165) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/netbios.rules(166) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/smtp.rules(62) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/sql.rules(69) threshold (in rule) is deprecated; use detection_filter instead.
   - /etc/snort/rules/sql.rules(73) threshold (in rule) is deprecated; use detection_filter instead.


<br />
# STEP 2

## Looking at the web-client.rules file, I researched this one rule and the references to investigate what precisely this vulnerability could do.

Rule Location: /etc/snort/rules/web-client.rules

```alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (msg:"WEB-CGI /wwwboard/passwd.txt access"; flow:to_server,established; uricontent:"/wwwboard/passwd.txt"; nocase; reference:arachnids,463; reference:bugtraq,649; reference:cve,1999-0953; reference:cve,1999-0954; reference:nessus,10321; classtype:attempted-recon; sid:807; rev:11;)```

Vulnerability:  `WWWBoard has a default username and default password.`

CVE and NVD sites to confirm the vulnerability and risk level:
https://www.cve.org/CVERecord?id=CVE-1999-0954
https://nvd.nist.gov/vuln/detail/CVE-1999-0954


## Selecting two web attack signatures:

Here I decided to try and use the Damn Vulnerable Web Application (DVWA) to work this problem out by replicating a vulnerable site to try and trigger a web SQL attack SNORT rule. Here are the steps I implemented but could not successfully trigger any alerts.  Although a record was created, no logs were created.   

Created two rules in the /etc/snort/rules/local.rules file:
'''
alert tcp any any -> any 80 (msg:"SQL Injection - Select Keyword Detected in URL"; flow:to_server,established; content:"SELECT"; http_uri; nocase; sid:1000001; rev:1;)

alert tcp any any -> any 80 (msg:"SQL Injection - Union Select Detected in URL"; flow:to_server,established; content:"union+select"; http_uri; nocase; sid:1000002; rev:1;)
'''

After adding the rules to the file, I completed the following steps the config file and added the `local.rules` path to the snort.config file

sudo snort -T -c /etc/snort/snort.conf
sudo snort -q -A console -c /etc/snort/snort.conf
Using RDP, I accessed my GCP instance web browser, Firefox, and signed into DVWA.
In DVWA, completed two different SQL injections `?id=1+SELECT+1` or `?id=UNION+SELECT+1,2,3`

![image](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/9228e494-fa0c-4f83-862e-d2d34f0c5822)

![Screenshot 2023-11-13 at 5 48 44 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/f4875d9c-d889-4fb7-89a0-c2b211718a7e)

![Screenshot 2023-11-13 at 5 48 01 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/35f5f150-3697-4142-86b8-09ea4544636c)

![Screenshot 2023-11-13 at 5 48 07 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/4eee32bf-0a4b-42f8-9b34-e9033845e2f6)

At this point, NO alerts were printed automatically, nor were there any alerts in the `snort.log.1699919198` log file.

![Screenshot 2023-11-13 at 5 54 41 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/b26868dc-a0a5-4752-b765-aff394524fe2)


Step 2 Summary:
Step 2 presented its own set of challenges. Initially, I had to independently research how to explore the references mentioned, including the CVE, NVD, and Bugtraq sites. This was prompted by analyzing the web-*.rules, where I found references for further investigation. The major difficulty I encountered in the latter part of Step 2 was related to the rule configuration and its role in triggering alerts for my SQL-i attack using DVWA. I attempted to think outside the box, exploring methods beyond the lab's scope, such as utilizing a web server or hosting site. The issue likely stemmed from either the snort.config file or my rule setup. Despite my efforts, I was unable to resolve this aspect of Step 2.   



<br />

***Step 3 - Customer Snort Rule to trigger alerts for accessing google.com***

Added the customer google snort rule to `/etc/snort/rules/local.rules`

![Alt text](<Screenshot 2023-12-08 at 10.03.21 PM.png>)

Refreshed Snort running the command `sudo snort -T -c /etc/snort/snort.conf`

Started Snort using sudo `snort -q -A console -c /etc/snort/snort.conf`

   - This did not yield any alerts when opening Firefox and going to google.com

Stopped the scan, proceeded to start Snort using interface `ens4` when starting the scan `snort -i ens4 -q -A console -c /etc/snort/snort.conf`.

   - This did not yield any alerts when opening Firefox and going to google.com


Stopped the scan, proceeded to start Snort using interface `lo` when starting the scan `snort -i lo -q -A console -c /etc/snort/snort.conf`.

   - This did not yield any alerts when opening Firefox and going to google.com


<br />
<br />

# Questions:

1. In step 1, how did you modify the config file to make it work?

 - Ran the command sudo snort -c /etc/snort/snort.conf to check the SNORT configuration file to look for any files containing a deprecated format. For each deprecated result, I would access the specific .rules file and apply the # at the beginning of the rule to comment the rule out.

<br />

2. In step 2, describe the two attack signatures you chose and explain the corresponding rules against them. How did you attempt to trigger the alert? How did snort process your requests?

- See Step 2.  


<br />
3. In step 3, copy/paste your new rule here. How did you confirm that your rule was enforced by snort?

   - alert tcp any any -> any 80 (msg:"Google.com visit detected"; content:"Host|3a| www.google.com"; sid:1000001;)
