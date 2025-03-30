***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 7 <br>
Due: March 1, 2024 <br>

---

<br>

## Q1. PCAP: Development.wse.local is a critical asset for the Wayne and Stark Enterprises, where the company stores new top-secret designs on weapons. Jon Smith has access to the website and we believe it may have been compromised, according to the IDS alert we received earlier today. First, determine the Public IP Address of the webserver?

In attempt to find the `Development.wse.local`, first needed to filter for `http` traffic.  The first time `Development.wse.local` packets started to appear was in frame 4197.  Now that I was able to analyze further traffic I came to conclude this site was built using Word Press.  Now, in an effort to find the Public IP of the webserver, I navigated to `File > Export Objects > selecting HTTP` to access the `HTTP object list`.  After putting in `wp-login.php` I was able to find the site ``Development.wse.local` and the Public IP address of the webserver `74.204.41.73`.

![alt text](<Screenshot 2024-03-06 at 12.00.23 PM.png>)

![alt text](<Screenshot 2024-03-06 at 12.01.47 PM.png>)


<br>

## Q2. PCAP: Alright, now we need you to determine a starting point for the timeline that will be useful in mapping out the incident. Please determine the arrival time of frame 1 in the "GrrCON.pcapng" evidence file.

Looking at the first frame of the `GrrCON.pcapng`, I was able to determine the UTC Arrival Timee `Sep 10, 2013 22:51:07.894237000 UTC`.

![alt text](<Screenshot 2024-03-11 at 9.37.23 AM.png>)


<br>

## ***QUESTIONS 3 & 4 ARE COMBINED RESPONSES***

## Q3. PCAP: What version number of PHP is the development.wse.local server running?

## Q4. PCAP: What version number of Apache is the development.wse.local web server using?

In order for me to narrow my search, I first checked the `HTTP object list` for the `development.wse.local` server.  Using the first frame that it populated, I was able to find the PHP and Apache versions numbers;

PHP Version:        5.3.2
Apache Version:     2.2.14

![alt text](<Screenshot 2024-03-11 at 10.37.58 AM.png>)

![alt text](<Screenshot 2024-03-11 at 10.42.42 AM.png>)


<br>

## Q5. IR: What is the common name of the malware reported by the IDS alert provided?

Using the provided snapshot `IR-Alert.png` , we can determine the `Zeus` malware was detected in the IDS.    

`grrcon-virtual-
172.16.0.109    74.125.225.112  ET TROJAN Zeus Bot GET to Google checking Internet connectivity 09/11/2013`

![alt text](<Screenshot 2024-03-11 at 2.38.25 PM.png>)


<br>

## Q6. PCAP: Please identify the Gateway IP address of the LAN because the infrastructure team reported a potential problem with the IDS server that could have corrupted the PCAP

I was able to locate the Gateway IP `172.16.0.1` by first completing a ARP filter.  After analyzing the packets there a numerous connections looking for `172.16.0.1`.  In an effort to further identify the Gateway IP, I also searched the following `Statistics > Endpoints`, selecting the IPv4 tab, we can further determine the connection and the total packets the Gateway communicated.

![alt text](<Screenshot 2024-03-12 at 10.16.09 AM.png>)

![alt text](<Screenshot 2024-03-12 at 10.40.50 AM.png>)


<br>

## Q7. IR: According to the IDS alert, the Zeus bot attempted to ping an external website to verify connectivity. What was the IP address of the website pinged?

Based on the `IR-Alert.png` image, the external site that was pinged was `74.125.225.112`.

![alt text](<Screenshot 2024-03-13 at 11.34.48 AM.png>)

<br>

## Q8. PCAP: It’s critical to the infrastructure team to identify the Zeus Bot CNC server IP address so they can block communication in the firewall as soon as possible. Please provide the IP address?

Using the specific filter, `ip.addr == 172.16.0.109 && http`.  After applying the filter and analyzing the packets from the result of applying the filter I see an unusual connection that appears to be an executable from host IP `88.198.6.20`.  Furthering the investigation, I edited the filter to add the host IP, `ip.addr == 172.16.0.109 && ip.addr == 88.198.6.20 && http`.  I can assess there was an attempt to access `172.16.0.109` and thereafter another executable being done followed by pultiple POST connections being applied.   Further anlaysis, it appears the executables were done through attempts to access some type of image (ex. jpeg or gif).  

![alt text](<Screenshot 2024-03-12 at 2.17.11 PM.png>)

![alt text](<Screenshot 2024-03-13 at 9.03.50 AM.png>)

![alt text](<Screenshot 2024-03-13 at 9.07.12 AM.png>)

![alt text](<Screenshot 2024-03-13 at 9.08.44 AM.png>)


<br>

## Q9. PCAP: The infrastructure team also requests that you identify the filename of the “.bin” configuration file that the Zeus bot downloaded right after the infection. Please provide the file name?

As mentioned about in Q8 from the onset analysis, there was an executable `bt.exec` that was done and in that I believe `cf.bin` was then downloaded.  

![alt text](<Screenshot 2024-03-13 at 10.34.02 AM.png>)


<br>

## Q10. PCAP: No other users accessed the development.wse.local WordPress site during the timeline of the incident and the reports indicate that an account successfully logged in from the external interface. Please provide the password they used to log in to the WordPress page around 6:59 PM EST?

Using the `ip.addr == 172.16.0.108 && http` filter, I was a able to identify the External IP Host `74.204.41.73` the user was successfully able to login using the username `Jsmith` and password `wM812ugu`.  In the following packet I was further correlate the time zone differential with 18:59 EST to 17:59 CDT, which is a one hour difference. 

![alt text](<Screenshot 2024-03-14 at 10.58.34 PM.png>)

<br>

## Q11. PCAP: After reporting that the WordPress page was indeed accessed from an external connection, your boss comes to you in a rage over the potential loss of confidential top-secret documents. He calms down enough to admit that the design's page has a separate access code outside to ensure the security of their information. Before storming off he provided the password to the designs page “1qBeJ2Az” and told you to find a timestamp of the access time or you will be fired. Please provide the time of the accessed Designs page?

Using the `HTTP object list`, I was able to just do a search for `developement.wse.local` to narrow my search for the password `1qBeJ2Az`.  Now I can see the UTC Arrival Time, `Sep 10, 2013 23:04:04.005564000 UTC`

![alt text](<Screenshot 2024-03-14 at 10.22.36 PM.png>)

![alt text](<Screenshot 2024-03-14 at 10.25.52 PM.png>)


<br>

## Q12. PCAP: What is the source port number in the shellcode exploit? Dest Port was 31708 IDS Signature GPL SHELLCODE x86 inc ebx NOOP

Using the porvided `Dest Port 31708`, I was able to apply a custom filter, `tcp.port == 31708 || udp.port == 31708`, in a effort to find the Source Port, `39709`.

![alt text](<Screenshot 2024-03-14 at 10.51.54 PM.png>)


<br>

## Q13. PCAP: What was the Linux kernel version returned from the meterpreter sysinfo command run by the attacker?

The following were the steps used to find the kervnal version `2.6.32-38-server`.

- Using the `Find Packet` feature by clicking the Edit tab.
- Search for the string `sysinfo`
- Using the first packet, right click and follow the tcp stream..
- Do a search for `sysinfo`.

![alt text](<Screenshot 2024-03-15 at 12.11.40 PM.png>)

![alt text](<Screenshot 2024-03-15 at 12.12.53 PM.png>)


<br>

## Q14. PCAP: What is the value of the token passed in frame 3897?

Searched for packet 3897. Found token value `b7aad621db97d56771d6316a6d0b71e9`.

![alt text](<Screenshot 2024-03-15 at 12.25.02 PM.png>)


<br>

## Q15. PCAP: What was the tool that was used to download a compressed file from the webserver?

Using the filter `http.request.method == GET:` to analyze packets, i was able to find that in frame `5304` it appears this is the only packet containing a compressed file extension `tar.gz`.  Further analyzing the packet, I can see the file was downloaded using the `wget`.

![alt text](<Screenshot 2024-03-16 at 4.21.19 PM.png>)


<br>

## Q16. PCAP: What is the download file name the user launched the Zeus bot?

Applying the same filter from `Q8`, `ip.addr == 172.16.0.109 && ip.addr == 88.198.6.20 && http`, I can see the file name `bt.exe`.   

![alt text](<Screenshot 2024-03-16 at 5.14.53 PM.png>)


<br>


## ***NOTE: For Questions 17-21 I only followed the walk-through as I didn't know how to access a Ubuntu 10 using Apple Macbook M1/Silicon chip***


## Q17. Memory: What is the full file path of the system shell spawned through the attacker's meterpreter session?

Accessing terminal, I could have ran the following command to find the full file path of the system shell spawned through the attacker's meterpreter session:

`vol.py -f Ubuntu10-4/webserver.vmss --profile=LinuxDFIRwebsvrx64 linux_psaux`

Answer: `/bin/sh`

![alt text](<Screenshot 2024-03-16 at 5.23.44 PM.png>)

<br>

## Q18. Memory: What is the Parent Process ID of the two 'sh' sessions?

In the process to search for the process ID of the two `sh` sessions, i need to first use the following command `vol.py -f Ubuntu10-4/webserver.vmss --profile=LinuxDFIRwebsvrx64 linux_pslist`.  Reviewing the results, I can assert ssh sessions have a parent ID `1042`, which is apache2

![alt text](<Screenshot 2024-03-16 at 5.33.00 PM.png>)


<br>

## Q19. Memory: What is the latency_record_count for PID 1274?

In the write-up used it referrenced the command used to identify what the `latency_record_count for PID 1274`.  The command used is `vol.py -f Ubuntu10-4/webserver.vmss --profile=LinuxDFIRwebsvrx64 linux_volshell` but still needing to plug in PID `1274`.  The following screenshot will provide the full steps that were taken

![alt text](<Screenshot 2024-03-16 at 5.45.51 PM.png>)

<br>

## Q20. Memory: For the PID 1274, what is the first mapped file path?

The following command was used to locate the first mapped file path, `vol.py -f Ubuntu10-4/webserver.vmss --profile=LinuxDFIRwebsvrx64 linux_proc_maps --pid 1274`, which is `/bin/dash`.   

![alt text](<Screenshot 2024-03-16 at 5.47.56 PM.png>)

![alt text](<Screenshot 2024-03-16 at 5.48.09 PM.png>)


<br>

## Q21. Memory:What is the md5hash of the receive.1105.3 file out of the per-process packet queue?

In the effor to find the md5hash, we need to modify the previous commands to include the `linux_pkt_queues` plugin, `vol.py -f Ubuntu10-4/webserver.vmss --profile=LinuxDFIRwebsvrx64 linux_pkt_queues -D pkts`.  The result is md5 hash - `184c8748cfcfe8c0e24d7d80cac6e9bd`.   


![alt text](<Screenshot 2024-03-16 at 5.49.56 PM.png>)


