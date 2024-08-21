***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 5 <br>
Due: March 1, 2024 <br>

---

<br>

## Point 1 - Supplicant to Authenticator (EAPoL) using the `wirelesseapolfiltered.pcap`

<br>

As the article provide guidance to follow along, I was able to utilize the provided filtering for the protocol, supplicant, and authenticator using the following filter `eapol && wlan.addr == e2:55:2d:f2:d1:54 && wlan.addr == 00:9a:cd:b7:c9:f0`.  The output after applying the filter provides all the EAPoL messages as a result: 

![alt text](<Screenshot 2024-03-03 at 6.38.28 PM.png>)

<br>

***EAP-Identity Response:***
In the process of capturing the client device (supplicant) and the access device (authenticator), I was able to find `Frame 29` identifying the supplicant of the user `employeealex`.

![alt text](<Screenshot 2024-03-03 at 5.13.38 PM.png>)

<br>

***EAP Auth Method Negotiation and Credential Exchange:***

Here we can see the handshake negotioant and the exchange of credentials, i.e. server certificate.  The handshake is in frames 40,44, and 48.   

![alt text](<Screenshot 2024-03-03 at 7.04.59 PM.png>)

![alt text](<Screenshot 2024-03-03 at 7.05.10 PM.png>)

<br>

***EAP Success(wired and wireless) and 4 Way Handshake (when the client is wireless):***

Upon the completion of the handshake and the client has been successfully authenticated and authorized, the `EAP Success` message should have been received.  In the following image, we can see that in `frame 78` indicates the `EAP Success` message.   

![alt text](<Screenshot 2024-03-03 at 7.10.20 PM.png>)

<br>
<br>


## Point 2 - Authenticator to Authentication Server (RADIUS) using the `wiredradiusfiltered.pcap`

<br>

The following filters for the access devices and the RADIUS server which is comprised of Access-Requests with Access-Challenges from the RADIUS server: 

`radius && ip.addr == 10.10.1.37 && ip.addr == 10.10.0.102`

*Note - all of the communication between the client and server during authentication is encapsulated in a RADIUS request.*


***The initial Access-Request packet:***

In `Frame 31` we can see the information in the `RADIUS` protocol and further assert that Authenticator IP `10.10.0.102` is using the username `employeealex`. Other useful information could also be found in the frame in the following sections `NAS-Port-Type, Service-Type, and Called-Station-ID`

![alt text](<Screenshot 2024-03-03 at 8.10.40 PM.png>)

Another important useful piece of informaiton could be found in the `NAS-IP-Address` section.  It could be used to differentiate Radius clients in the Radius server.

![alt text](<Screenshot 2024-03-03 at 8.49.13 PM.png>)


In `Frame 55` we can identify a successful authentication. The type of policy this connection triggered was a `BYOD-Access` group policy.  

![alt text](<Screenshot 2024-03-03 at 8.57.48 PM.png>)


<br>

***RADIUS Accounting Messages:***

<br>

In obverving, frames 55 (Access-Accept), 56 (Accounting-Request), and 57 (Accounting-Response) I was able to correlate the UDP ports getting interchanged from 1812 to 1813 when the commuications changes to `Accounting`.  In addition, if the communications disconnected alternatively we would then see a `Accounting-Stop` message.  Other pieces of information here could be found in `Event-Timestamps`, `Session-IDs`, and `Framed-IP-Address`.

![alt text](<Screenshot 2024-03-03 at 9.17.44 PM.png>)











