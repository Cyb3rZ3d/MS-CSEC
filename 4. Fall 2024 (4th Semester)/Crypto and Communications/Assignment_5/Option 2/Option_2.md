
```
Assignment Instructions:

1) Complete a "Hello World" on the IBM Quantum Computing Array or

2) Diagram 2 different types of TCP based cryptographic conversations from Wireshark - instantiate a connection, pass data, tear down while capturing and analyzing the data to document what is happening.

Provide sufficient narrative and screenshots to document your journey. Justify the value in your submission.
```


# Option 2: Diagram 2 different types of TCP based cryptographic conversations from Wireshark - instantiate a connection, pass data, tear down while capturing and analyzing the data to document what is happening.

<br>

# ***1st Diagram: ***
The following were preliminary steps to query the DNS and any and all associated IPs to `cnn.com`.  Some steps might seem like redundant steps were taken, but these steps were done in attept to ensure I matched IPs and were alike throughout.

1. Using terminal I used `dig` and `nslookup`to query the DNS and the associated IP addresses:

        dig cnn.com

        nslookup cnn.com

    ![alt text](<Screenshot 2024-11-24 at 3.36.35 PM.png>)

    ![alt text](<Screenshot 2024-11-24 at 3.35.10 PM.png>)


2. Using Wireshark I did a dns query for `cnn.com` to capture all associated IPs to the site:

        dns.qry.name == "cnn.com"

    ![alt text](<Screenshot 2024-11-24 at 3.40.14 PM.png>)

        tcp.port == 443 && (ip.addr == 151.101.67.5 || ip.addr == 151.101.195.5 || ip.addr == 151.101.131.5 || ip.addr == 151.101.3.5)


CNN site I visited:

    cnn > US
    cnn > world > Unidentified drones spotted over thress US Air Force bases in Britain.


https://cloud.google.com
