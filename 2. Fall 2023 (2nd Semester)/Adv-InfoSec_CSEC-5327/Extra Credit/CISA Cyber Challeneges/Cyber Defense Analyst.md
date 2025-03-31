Ruben Valdez <br />
CSEC 5327 | Adv. InfoSec <br />
Prof. Alsmadi <br />
Assignment: Extra Credit | Cyber Defense Analyst <br />
https://trycyber.us/challenges/

<br />

Intro:

In this challenge, we'll analyze pcap files using Wireshark to determine if brute force attacks were being executed against the client.  In this lab environment, CISA set up a VM using Ubuntu 22.04.

PCAP file locations are on the Desktop in the folder for `Materials`:

![Screenshot 2023-11-19 at 11 11 12 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/74371525-6762-4037-a22d-23d2399c3f60)

![Screenshot 2023-11-19 at 11 11 33 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/a3e32b09-694b-4654-9d8f-cc1fb69414c7)



1. bruteforce-1.pcap:

Using Wireshark, I set the filter to view FTP, and immediately, I was able to determine there was some unusual activity.  It appears there were several login attempts to access the admin user account from IP `10.1.20.5`.

![Screenshot 2023-11-19 at 10 25 09 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/ab3f12b7-56d0-49b1-816a-55e8fe0a6e6e)



2. bruteforce-2.pcap:

I  repeated the same steps to view the 1st pcap.   I set the same filter, and immediately again, I could determine some unusual activity.  It appears there were several login attempts to access the admin user account from IP `10.1.20.98`.
  
![Screenshot 2023-11-19 at 10 09 22 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/f0f2da92-cc58-4866-9335-54ea910cfe85)



3. Reporting

After each pcap analysis, I had to complete the reporting feature of the challenge and answer the questions of what was analyzed during the challenge.

![Screenshot 2023-11-19 at 10 32 02 PM](https://github.com/Cyb3rZ3d/Adv-InfoSec_CSEC-5327/assets/108482007/65167c9e-4493-42b2-8c6f-57bade45ef39)




Conclusion:

In conclusion, this challenge was a quick assessment to determine if a brute force attack had been initiated against a system or systems.   It was further determined within this challenge that it is confirmed there were attempts to brute force FTP.   


