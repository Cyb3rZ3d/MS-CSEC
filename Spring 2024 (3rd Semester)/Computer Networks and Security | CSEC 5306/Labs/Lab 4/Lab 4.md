***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 4 - 'mi-img' <br>
Due: Feb. 12, 2024 <br>



Went to `https://packettotal.com` and uploaded the following pcaps:

```
hydra_telnet.pcap
nmap.pcap
```

![alt text](<Screenshot 2024-02-20 at 3.37.27 PM.png>)


# hydra_telnet.pcap

At first glance using the `Network Graph`, it appears there are a number of different connections.  I was able to apply filters for `Overlays` and enbale `Malicious Traffic` and `Suspicous Traffic`.  After applying the filters, I was able to identify the `Host and Link Details` and recognized there was a `Suspicious` Severity. 

![alt text](<Screenshot 2024-02-20 at 3.44.18 PM.png>)


We can assert, using the `Timeline Analysis` feature, the time table for the suspicious activity took place in the late morning 11:48 AM between the following connections:

![alt text](<Screenshot 2024-02-20 at 3.51.13 PM.png>)

