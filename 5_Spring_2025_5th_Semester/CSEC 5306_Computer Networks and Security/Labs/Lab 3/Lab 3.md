***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 3 - 'mi-img' <br>
Due: Feb. 9, 2025<br>


# `MI-IMG` Injection

## Instructions:

In this lab, you are expected to:
    
    (1) pick 1 attack mentioned in the documents attached

    (2) follow the traces of the attack in the pcap files
    
    (3) demonstrate the lifecycle of the attack with a small report/screenshots
    
    (4) Demo anyone besides the one(s) used in the demo

You can read some information about the dataset in the pdf files attached.

Hint 1: Familiarize yourself with Wireshark filters, very powerful and can give you quick shortcuts and save you time. For example, I use ( http && (media || data-text-lines)) filter to find packets of HTTP with data (very relevant to many web attacks), at least it can be a good starting point. 

Hint 2: I may use (javascript) to search for in [string, packet bytes], to search for possible Javascripts code injects.



## Lab Issues/Notes:***

1. Using Wireshark filtering, unable to filter `frame contrains <http code>`.  
    
    Ex. frame contains 302
    
    ![alt text](<Screenshot 2024-02-10 at 9.38.31 PM.png>)

<br>
<br>

## 1994.pcap

Initial analysis of all the packets, I can see there are some timestamps that appear unusual as showing a negative number (ex. -5.3594). Other naked eye concernes here is that I see TCP unseen segments and retransmissions.

Frame 17, there is a connection made from 0.0.0.0 to the Host IP 120.198.233.14 that appear to be 

![alt text](<Screenshot 2024-02-10 at 8.12.14 PM.png>)

Used the following TCP filters `tcp.stream eq 0` and `tcp.stream eq 1` to find frames that would confirm a `GET` request and a `HTTP 302 Found`

![alt text](<Screenshot 2024-02-10 at 11.20.34 PM.png>)

Frame 21, clearly indicates `HTTP 302 Found Server` at http:120.198.231.23
    
![alt text](<Screenshot 2024-02-10 at 11.11.10 PM.png>)

Not much detail was provided when attempting to `Follow TCP Stream`.  Within the stream, I don't visibly see the server IP; although, I can identify the Host IP 120.198.233.14

![alt text](<Screenshot 2024-02-10 at 11.18.10 PM.png>)

<br>
<br>

## 1995.pcap

<br>

Initial analysis of all the packets I see TCP Out-of-Order and RST packets indicating theres a reconnection attemtp.

Frame 9, there is a connection made from 0.0.0.0 to the Host IP 120.198.233.14 that appear to be from the same IP as mention before in the 1994.pcap, `HTTP 302 Found Server` at http:120.198.231.23.

![alt text](<Screenshot 2024-02-10 at 8.11.34 PM.png>)


- Used the following TCP filters `tcp.stream eq 0` to find frames that would confirm a `GET` request and a `HTTP 302 Found`.  In an effort to ensure there were no other TCP streams I attempted to filter `tcp.stream eq 1` but no results were given.

    ![alt text](<Screenshot 2024-02-10 at 11.44.25 PM.png>)

- Frame 9, Follow TCP Stream

![alt text](<Screenshot 2024-02-10 at 11.45.35 PM.png>)


