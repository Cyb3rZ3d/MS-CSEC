***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Lab 3 - 'mi-img' <br>
Due: Feb. 12, 2024 <br>


# `MI-IMG` Injection


## Lab Issues/Notes:***

1. Using Wireshark filtering, unable to filter `frame contrains <http code>`.  
    
    Ex. frame contains 302
    
    ![alt text](<Screenshot 2024-02-10 at 9.38.31 PM.png>)

<br>
<br>

## 1994.pcap

![alt text](<Screenshot 2024-02-10 at 8.12.14 PM.png>)

<br>

- Used the following TCP filters `tcp.stream eq 0` and `tcp.stream eq 1` to find frames that would confirm a `GET` request and a `HTTP 302 Found`

    ![alt text](<Screenshot 2024-02-10 at 11.20.34 PM.png>)

- Here, we can clearly identify the `HTTP 302 Found Server`
    
    ![alt text](<Screenshot 2024-02-10 at 11.11.10 PM.png>)

- Not much detail was provided when attempting to `Follow TCP Stream`.

    ![alt text](<Screenshot 2024-02-10 at 11.18.10 PM.png>)

<br>
<br>

## 1995.pcap

<br>

![alt text](<Screenshot 2024-02-10 at 8.11.34 PM.png>)

<br>

- Used the following TCP filters `tcp.stream eq 0` to find frames that would confirm a `GET` request and a `HTTP 302 Found`.  In an effort to ensure there were no other TCP streams I attempted to filter `tcp.stream eq 1` but no results were given.

    ![alt text](<Screenshot 2024-02-10 at 11.44.25 PM.png>)

- Frame 9, Follow TCP Stream

![alt text](<Screenshot 2024-02-10 at 11.45.35 PM.png>)