Ruben Valdez <br>
CSEC 5311 | Big Data Analysis and Security <br>
Prof. Hossain, Tamjid <br>
Bonus In-Class _ Lab 3

<br><br>


# Creating a digital watermarking using `OpenStego`

1. Generated a signature

    ![alt text](<Screenshot 2025-03-28 215449.png>)

    - Signature file successfully generated and saved

        ![alt text](<Screenshot 2025-03-28 215537.png>)


2. Embed watermark using my generated signature

    ![alt text](<Screenshot 2025-03-28 215827.png>)

    - The file I watermarked is a photo of my last Naval squadron I was attached to.

        ![alt text](VFA103.jpeg)
    
    - Confirmation watermark was created

        ![alt text](<Screenshot 2025-03-28 215901.png>)

        ![alt text](<Screenshot 2025-03-28 215917.png>)

3. File Watermark verification 

    ![alt text](<Screenshot 2025-03-28 220247.png>)

    - Because the passphrase used (CSEC5311) was a weak, the strength percentage was at 12%.  Had I of created a longer passphrase, the strength percentage would have been higher.  

        ![alt text](<Screenshot 2025-03-28 220301.png>)