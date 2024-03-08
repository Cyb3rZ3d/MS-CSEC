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








<br>

## Q3. PCAP: What version number of PHP is the development.wse.local server running?


<br>

## Q4. PCAP: What version number of Apache is the development.wse.local web server using?


<br>

## Q5. IR: What is the common name of the malware reported by the IDS alert provided?


<br>

## Q6. PCAP: Please identify the Gateway IP address of the LAN because the infrastructure team reported a potential problem with the IDS server that could have corrupted the PCAP


<br>

## Q7. IR: According to the IDS alert, the Zeus bot attempted to ping an external website to verify connectivity. What was the IP address of the website pinged?


<br>

## Q8. PCAP: It’s critical to the infrastructure team to identify the Zeus Bot CNC server IP address so they can block communication in the firewall as soon as possible. Please provide the IP address?


<br>

## Q9. PCAP: The infrastructure team also requests that you identify the filename of the “.bin” configuration file that the Zeus bot downloaded right after the infection. Please provide the file name?


<br>

## Q10. PCAP: No other users accessed the development.wse.local WordPress site during the timeline of the incident and the reports indicate that an account successfully logged in from the external interface. Please provide the password they used to log in to the WordPress page around 6:59 PM EST?


<br>

## Q11. PCAP: After reporting that the WordPress page was indeed accessed from an external connection, your boss comes to you in a rage over the potential loss of confidential top-secret documents. He calms down enough to admit that the design's page has a separate access code outside to ensure the security of their information. Before storming off he provided the password to the designs page “1qBeJ2Az” and told you to find a timestamp of the access time or you will be fired. Please provide the time of the accessed Designs page?


<br>

## Q12. PCAP: What is the source port number in the shellcode exploit? Dest Port was 31708 IDS Signature GPL SHELLCODE x86 inc ebx NOOP


<br>

## Q13. PCAP: What was the Linux kernel version returned from the meterpreter sysinfo command run by the attacker?


<br>

## Q14. PCAP: What is the value of the token passed in frame 3897?


<br>

## Q15. PCAP: What was the tool that was used to download a compressed file from the webserver?


<br>

## Q16. PCAP: What is the download file name the user launched the Zeus bot?


<br>

## Q17. Memory: What is the full file path of the system shell spawned through the attacker's meterpreter session?


<br>

## Q18. Memory: What is the Parent Process ID of the two 'sh' sessions?


<br>

## Q19. Memory: What is the latency_record_count for PID 1274?


<br>

## Q20. Memory: For the PID 1274, what is the first mapped file path?


<br>

## Q21. Memory:What is the md5hash of the receive.1105.3 file out of the per-process packet queue?






