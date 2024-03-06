***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 6 <br>
Due: March 1, 2024 <br>

---

<br>



Using the Wireshark Protocol Hierarchy we can see and general summary of the entirety of the pcap's protocols and packets.

![alt text](<Screenshot 2024-03-05 at 10.25.17 AM.png>)


## Question 1 : What is the FTP password?

Since the questions is regarding FTP, I first needed to filter the pcap traffic for FTP.  After analyzing the data, I assessed that in frames 486 - 502 the client `192.168.1.20` successfully accessed and logged into to the server `192.168.1.26` using the credentials `Kali` for the username and `AfricaCTF2021` as the password.  Some further context, we further identify that FTP is unencrypted because the text is in clear text.

![alt text](<Screenshot 2024-03-05 at 11.10.40 AM.png>)

<br>

## Question 2: What is the IPv6 address of the DNS server used by 192.168.1.26?

- We need to take a layered approach in order to find the IPv6 address of the DNS server: 

    - We must find the MAC address of the server `192.168.1.10` using the following technique in Wireshare.  The following are the steps I used to find the MAC address:

        - Using frame 203 locate the `Ethernet II` section of the capture and here is how you can find the source MAC address

            ![alt text](<Screenshot 2024-03-05 at 1.50.02 PM.png>)

        - Highlighting/Clicking frame 203, in the menu bar select `Statistics` then select `Conversations`.  Upon initial review, we can see a few tabs `Ethernet, IPv4, IPv6, TCP, and UDP`.

            - Reviewing the above screenshot we can confirm the identity of `Address A` for each tab is the MAC address of `ca:0b:ad:ad:20:ba` that is associated to IPv4 `Src: 192.168.1.10`.

                ![alt text](<Screenshot 2024-03-05 at 1.12.42 PM.png>)

                ![alt text](<Screenshot 2024-03-05 at 1.18.19 PM.png>)

                ![alt text](<Screenshot 2024-03-05 at 1.19.46 PM.png>)

        - Finally, in the IPv6 tab, we can see the address - `fe80::c80b:adff:feaa:1db7`


<br> 

## Question 3: What domain is the user looking up in packet 15174?

In frame 15174, the frame is a query to the `www.7-zip.org` domain where we can see there is a response in frame 15190.  In frame 15190, we can see the response from the domain is `www.7-zip.org: type A, class IN, addr 159.65.89.65`

![alt text](<Screenshot 2024-03-05 at 3.25.59 PM.png>)

![alt text](<Screenshot 2024-03-05 at 3.25.24 PM.png>)


<br>

## Question 4: How many UDP packets were sent from 192.168.1.26 to 24.39.217.246?

Needing to identify the number of UDP packets there might be in the pcap, we need to efficiently apply the following filter, `udp && ip.src == 192.168.1.26 && ip.dst == 24.39.217.246`.  After the filter has been applied, we can visibly see there are `10` UDP packets.   

![alt text](<Screenshot 2024-03-05 at 3.32.39 PM.png>)


<br>

## Question 5: What is the MAC address of the system being monitored?

Using the same filters as before, we know the monitorying system is the IPv4 , the MAC address is clear that it is `c8:09:a8:57:47:93` 

![alt text](<Screenshot 2024-03-05 at 3.46.57 PM.png>)


<br>

## Q6: What was the camera model name used to take picture 20210429_152157.jpg ?

In order to locate the model name of the camera, we first need to filter for `ftp-data` then look for the image name `20210429_152157.jpg`.  Choosing a random frame containing the image `20210429_152157.jpg`, I then proceeded to follow the `TCP Stream` and then saved the image as a raw file, `lab6.raw`.  I then needed to view the metadata of the of the file in order to gather the model name.  I decided to use the following site, `https://exifinfo.org` to view the metadata.  After uploading the `lab6.raw` file, I was able to gather the model name, `LM-Q725K`, of the camera used to take `20210429_152157.jpg`

![alt text](<Screenshot 2024-03-05 at 9.02.21 PM.png>)

![alt text](<Screenshot 2024-03-05 at 9.00.32 PM.png>)

![alt text](<Screenshot 2024-03-05 at 8.51.31 PM.png>)


<br>

## Q7: What is the server certificate public key that was used in TLS session: da4a0000342e4b73459d7360b4bea971cc303ac18d29b99067e46d16cc07f4ff?

I was able to apply the following filter, `tls.handshake.type==2`, to view the TLS sessions. After the filter was applied I was then able to do a `Find my Packet` search.  Modified the search for `Packet Details` which is one of three selections, then did a search for `da4a0000342e4b73459d7360b4bea971cc303ac18d29b99067e46d16cc07f4ff`.  After the search it was then clearer I could locate the `Handshake Protocol: Server Key Exchange` and find the `pubkey: 04edcc123af7b13e90ce101a31c2f996f471a7c8f48a1b81d765085f548059a550f3f4f62ca1f0e8f74d727053074a37bceb2cbdc7ce2a8994dcd76dd6834eefc5438c3b6da929321f3a1366bd14c877cc83e5d0731b7f80a6b80916efd4a23a4d`.

![alt text](<Screenshot 2024-03-05 at 10.42.36 PM.png>)

![alt text](<Screenshot 2024-03-05 at 10.42.08 PM.png>)


<br>

## Q8: What is the first TLS 1.3 client random that was used to establish a connection with protonmail.com?

Using the linke `https://unit42.paloaltonetworks.com/unit42-customizing-wireshark-changing-column-display/` to guide in creating columnes.  I added the columne `Host` columne and this is to view bother the `Server Name` and `Host`.

![alt text](<Screenshot 2024-03-05 at 10.34.30 PM.png>)


Proceeding further, I now could filter for `TLS` and do a packet search for `protonmail.com`.  The first result of the server name starts in frame `17992`.  Following the packet to observe the `Random: 24e92513b97a0348f733d16996929a79be21b0b1400cd7e2862a732ce7775b70`.  

![alt text](<Screenshot 2024-03-05 at 10.55.13 PM.png>)


<br>

## Q9: What country is the MAC address of the FTP server registered in? (two words, one space in between)

To find the country of the MAC address of the FTP server is registered in, we much find the MAC address.  Using the `ftp` filter, I chose frame 486 as this accessing a FTP server.  After review of the packet details I was able to find the MAC address, `08:00:27:a6:1f:86`, for the IPv4 address `192.168.1.20`.  Now that we know the MAC address, we can proceed to the following site, `https://mac-address.alldatafeeds.com/mac-address-lookup`, to retrieve the MAC Address vendor details about the device.  The results, we can identify and confirm the vendor details for this device, but the biggest question here is the country of the device it was registered in, we can confirm it was in the `United States`.  

![alt text](<Screenshot 2024-03-05 at 11.19.31 PM.png>)

![alt text](<Screenshot 2024-03-05 at 11.16.45 PM.png>)


<br>

## Q10: What time was a non-standard folder created on the FTP server on the 20th of April? (hh:mm)

To locate the time non-standard folder created on the FTP server on the 20th of April, I needed to apply the filter for the `ftp-data` protocol and find the list.  I see in frame 530, in the Info column, there is text that reads `List`.  In the packet details, I can see there's a section for Line-based text data.  Visually, I can see a list of folders and there permissions, and the dates and time.  Correlating the information, I can confirm there was a folder, `ftp` that was created `April 20th at 17:53`.

![alt text](<Screenshot 2024-03-05 at 11.22.44 PM.png>)


<br>

## Q11: What domain was the user connected to in packet 27300?

The steps I took to locate the domain of IP 172.67.162.206 was to first find frame 27300.  Copy the Dest IP `172.67.162.206` and in the tab `Statistic > Resolved Addresses`, paste the IP in the field and your domain name should populate.  In this case the user was connected to the `dfir.science` domain.

![alt text](<Screenshot 2024-03-05 at 11.33.22 PM.png>)

![alt text](<Screenshot 2024-03-05 at 11.37.13 PM.png>)