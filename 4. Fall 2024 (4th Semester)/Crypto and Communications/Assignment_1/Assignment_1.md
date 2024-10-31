Ruben Valdez <br>
Crypto and Communications _ CSEC 5323 <br>
Prof.: Dr. Jones, Robert <br>
Assignment: Crypto Potpourri <br>

---

 <br>

# Task 1: 

1. ***Reflect on the Grace Hopper videos newly available at https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/3884041/nsa-releases-copy-of-internal-lecture-delivered-by-computing-giant-rear-adm-gra/.***

2. ***What 2 things stood out to you the most from her lecture, and why? If she were alive today, what would she be talking about, and why, based on your experience? (50 points)***

    1. As a Navy veteran, I liked her introduction as using her hat as her identifier being a naval officer. Her witty banter about getting confused for either a pilot or flight attendant. Associating her identifier comment's made me think and what I think she was attempting to do as a message to the audience is that everything has an identifier.  

        The organization of identifies in everything we do in computing data and networking is something that is paramount in everything we do as cyber technicians.  

    2. Her explaination on Hardware, Software, Network Lifecycles

        In her explanation, I started to think to myself as the video was playing, back in R.Admiral's Hopper's time of all her work getting reactivated the hardware and software lifecycles weren't as clearly developed or just didn't exist then as it's being utilized now.  The way she proceeded to talk about the transfer of data securely over the wire and the speeds of it.  Technology and the speed of it were main challenges back in the day.  She clearly identifies the lack of lifecycle of systems when she was talking about how to take an island during a story about her attending the Navy War College.  Something that she identifies about her story is that the focuse was maintaining systems in the present but not preparing systems to be maintained for the future. Thus, the software, hardware, network lifecycles of systems.   
        
        
    3. The persistance of never stop asking even when told no when attempting to present or offer a solution for change or having a new concept.

        When R.Admiral Hopper talked about the persistance to never stop asking brought back something that I was told during my enlistment in the Navy, `Never stop asking why`.  This allowed me to always be curious.  Because of my curriosity, this has allowed me to gain greater insight's into different subject's.  `Never stop learning`.

    <br>

    - ***If she were alive today, what would she be talking about, and why, based on your experience?***

    In my opinion, with the experience I have had learning and working in cyber, I can relate to some of the applications she has described in her speech and presentation.  But I feel as though she would have a FIELD-DAY with presenting or learning about cloud computing. I feel like she'd bring notice on the transfer of data and security of applications and data in the current day vise how thing's worked abck in her career.  Just like how now, I feel like when setting up network's and applying new generational cloud networking and new generation firewall's would be foreign to her as everything would be easily accessible through a web-applications using a browser vise hardware.  



<br><br>

# Task 2: 

***Demonstrate completion of THREE cryptography emates from https://d2hie3dpn9wvbb.cloudfront.net/Cryptography/Crypto.html by providing a screenshot of completion.***

***You MUST include Diffie-Helman key exchange as one of the ones, the other two you may choose on your own. Please give a piece of feedback on each one. (30 points)***

1. ***Diffie-Helman Key Exchange:***

    The Diffie-Hellman key exchange is a fascinating and essential method for securely sharing cryptographic keys over a public network. It allows two parties to create a shared secret key, even if they've never met before, by each performing a simple mathematical operation. What stands out about Diffie-Hellman is its use of modular arithmetic to ensure that the key exchange remains secure from eavesdroppers. However, one downside is that it doesn't provide authentication, which means that additional steps are needed to verify the identities of the communicating parties. Overall, understanding Diffie-Hellman is crucial because it's a foundation for many encryption protocols used today.

    ![alt text](<Screenshot 2024-09-27 at 11.20.24 AM.png>)

    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br>

2. ***Hashing***

    Hashing is a really important concept in cybersecurity and helps ensure data hasn’t been changed when it’s sent or stored. A hash function works by taking any input and turning it into a unique, fixed-size output. This makes it a great way to check if data is still the same as when it was originally created. One of the best parts about hashing is that it’s a one-way process, meaning you can’t figure out the original input just from the hash value. However, it’s important to pick strong hashing algorithms because weaker ones can be vulnerable to attacks, like when different inputs create the same hash (collisions). Knowing how different hashing methods work and when to use them is key to keeping digital information secure.

    ![alt text](<Screenshot 2024-09-27 at 12.33.37 PM.png>)
    
    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br>

3. ***Public Key Infrastructure and Digital Certificates***

    Public Key Infrastructure (PKI) and digital certificates are crucial concepts in securing online communications. Learning about PKI really opened my eyes to how data is kept private and authentic on the internet. The use of digital certificates to verify identities adds a layer of trust to online transactions, especially since Certificate Authorities (CAs) act as the trusted third parties. I found it interesting how PKI not only encrypts data but also ensures its integrity and authenticity. However, the complexity of managing certificates and revocations, especially with Certificate Revocation Lists (CRLs), shows that while PKI is effective, it requires proper implementation and monitoring. Overall, understanding PKI and digital certificates is key for anyone wanting to dive deeper into cybersecurity.

    ![alt text](<Screenshot 2024-09-27 at 12.34.35 PM.png>)

    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br><br>

# Task 3:

1. ***Provide two examples of sending encrypted emails using gpg asymmetric key cryptography OR demonstrate a use of a hash such as reversing an encrypted password or any other function you feel appropriate. Please justify the 30 points if you elect to do a hash by telling me what you did, why you did it, and why you think you deserve the full amount of points. (60 points)***


1. Using Thunderbird, I added the following gmail accounts:

    - rvj.tamusa@gmail.com

        ![alt text](<Screenshot 2024-09-27 at 2.51.26 PM.png>)

    - valdez.ruben210@gmail.com

        ![alt text](<Screenshot 2024-09-27 at 2.51.08 PM.png>)


2. Generated OpenPGP key's for `rvj.tamusa@gmail.com` and `valdez.ruben210@gmail.com`

    ***REPEATE THE FOLLOWING STEPS FOR EACH ACCOUNT:***

    - Click the "three lines icon" in the top right corner > click tools > click OpenPGP Key Manager.

    - On the menu bar, click Generate > click New Key Pair

    - Keeping everything default except changing the `key size` to 4096 > then click Generate Key

    - Click confirm for the next screen.

    ![alt text](<Screenshot 2024-09-27 at 3.03.23 PM.png>)

    ![alt text](<Screenshot 2024-09-27 at 3.06.18 PM.png>)

3. Copied the public key for each account and sent an email.  

- Sent `rvj.tamusa@gmail.com` public key to `valdez.ruben210@gmail.com`

    ![alt text](<Screenshot 2024-09-27 at 3.14.32 PM.png>)

- Sent `valdez.ruben210@gmail.com` public key to `rvj.tamusa@gmail.com`

    ![alt text](<Screenshot 2024-09-27 at 3.15.03 PM.png>)


4.  Confirming the received emails from each account and viewing the source of the PGP key's

- Sent FROM `rvj.tamusa@gmail.com`; Recieved TO `valdez.ruben210@gmail.com`

    ![alt text](<Screenshot 2024-09-27 at 3.26.45 PM.png>)

    ![alt text](<Screenshot 2024-09-27 at 3.27.02 PM.png>)

- Sent FROM `valdez.ruben210@gmail.com`; Received TO `rvj.tamusa@gmail.com`

    ![alt text](<Screenshot 2024-09-27 at 3.32.58 PM.png>)

    ![alt text](<Screenshot 2024-09-27 at 3.33.26 PM.png>)



<br><br>

# Task 4:

1. ***Provide proof of your signup to the NSA Codebreaker Challenge at https://nsa-codebreaker.org/home . (10 points)***

    ![alt text](<Screenshot 2024-09-27 at 12.36.54 PM.png>)
