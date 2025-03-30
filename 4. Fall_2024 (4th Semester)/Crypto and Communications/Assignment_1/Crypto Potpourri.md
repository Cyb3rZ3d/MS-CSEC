Ruben Valdez <br>
Crypto and Communications _ CSEC 5323 <br>
Prof.: Dr. Jones, Robert <br>
Assignment: Crypto Potpourri <br>

---

 <br>

# Task 1: 

1. ***Reflect on the Grace Hopper videos newly available at https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/3884041/nsa-releases-copy-of-internal-lecture-delivered-by-computing-giant-rear-adm-gra/.***

2. ***What 2 things stood out to you the most from her lecture, any why? If she were alive today, what would she be talking about, and why, based on your experience? (50 points)***

    1. As a Navy veteran, I liked her introduction as using her hat as her identifier being a naval officer. Her witty banter about getting confused for either a pilot or flight attendant. Associating her identifier comment's made me think and what I think she was attempting to do as a message to the audience is that everything has an identifier.  

    Associates having a lousy job to maintain transportation as a whole to ho


Failed to value incorrect data informaiton.

She clearly identifies the lack of lifecycle of systems when she was talking about how to take an island.  Having to plan for the systems that will be needed in the futur and not the now.  

The persistance of never stop asking even when told no when attempting to present or offer a solution for change or having a new concept.




    2. 



<br><br>

# Task 2: 

***Demonstrate completion of THREE cryptography emates from https://d2hie3dpn9wvbb.cloudfront.net/Cryptography/Crypto.html by providing a screenshot of completion.***

***You MUST include Diffie-Helman key exchange as one of the ones, the other two you may choose on your own. Please give a piece of feedback on each one. (30 points)***

1. ***Diffie-Helman Key Exchange:***

    Communications over an unsecured network, the Diffie-Helman would be a decent choice to use. A vulnerability in this exchange would be a man-in-the-middle attack.  It was interesting to read the model and analogy it used to explain the tutorial and the math that's incorporated using it's formulas:

    - Ex. of the formula output:
        
        - Alice:    A = g^a mod p

        - Bob:      B = g^b mod p

    - Ex. of the fomula to calculate the common secret:

        - Alice:    S = B^a mod p

        - Bob:      S = A^b mod p
    
    ![alt text](<Screenshot 2024-09-27 at 11.21.41 AM.png>)

    ![alt text](<Screenshot 2024-09-27 at 11.20.24 AM.png>)

    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br>

2. ***Hashing***

    Hashing converts input data of any length into a fixed-size output, known as a hash value or digest, using mathematical or logical functions. This process operates directly on binary data, regardless of the input type. Hashing functions use predefined operations, like Boolean logic or summing binary numbers, to produce consistent, fixed-size digests. Algorithms like MD5 generate the same-sized output for any input, ensuring data integrity; any change in input results in a different hash. Hash functions are one-way processes, making it impossible to derive the original input from the output.
    

    Hash any type of data:

        - Downloaded file
        - Video
        - Image
        - Character string
        - Audio File
        - Password
        - Documents

    ![alt text](<Screenshot 2024-09-27 at 11.38.13 AM.png>)
    
    Hashing offer's SHA and MD5.  Using `check sum` is a way to check the integrity of the hash to ensure the file has not been modified in any way.   

    ![alt text](<Screenshot 2024-09-27 at 11.39.12 AM.png>)
    
    Depending on the SHA and MD5 size will output the size of the hash:

    ![alt text](<Screenshot 2024-09-27 at 11.36.58 AM.png>)

    ![alt text](<Screenshot 2024-09-27 at 12.33.37 PM.png>)
    
    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br>

3. ***Public Key Infrastructure and Digital Certificates***

    A Public Key Infrastructure (PKI) is a system that manages the distribution, verification, and revocation of public keys for secure communication. It involves Digital Certificates, issued by a trusted Certificate Authority (CA), which link a public key to its owner. These certificates contain information such as the public key, issuer details, and a digital signature. Types of Digital Certificates include personal, organizational, server, and developer certificates.

    PKI ensures secure data exchange by using a CA to authenticate identities. For example, when a user visits a secure website, the site presents a Digital Certificate that the user's browser validates, enabling encrypted communication using the public key. The PKI process involves creating a certificate signing request (CSR), which is verified by the CA and Registration Authority (RA) before issuing a certificate.

    PKI supports several key security functions: confidentiality, authentication, access control, non-repudiation, and integrity. Certificates can be revoked if compromised, listed in a Certificate Revocation List (CRL) checked by browsers during secure connections.

    ![alt text](<Screenshot 2024-09-27 at 12.34.35 PM.png>)

    <br>

    ***NOTE to professor:*** Not sure if I did this correctly, but there's no interactive questions to complete.  The screenshot just represents the end of the tutorial.  Not sure what to submit.  

<br><br>

# Task 3:

1. ***Provide two examples of sending encrypted emails using gpg asymmetric key cryptography OR demonstrate a use of a hash such as reversing an encrypted password or any other function you feel appropriate. Please justify the 30 points if you elect to do a hash by telling me what you did, why you did it, and why you think you deserve the full amount of points. (60 points)***




<br><br>

# Task 4:

1. ***Provide proof of your signup to the NSA Codebreaker Challenge at https://nsa-codebreaker.org/home . (10 points)***

    ![alt text](<Screenshot 2024-09-27 at 12.36.54 PM.png>)
