Ruben Valdez <br>
Crypto and Communications _ CSEC 5323 <br>
Prof.: Dr. Jones, Robert <br>
Assignment: Crypto Potpourri <br>
Due. Nov. 1, 2024.

---

 <br>

# Task 1:   Find and demonstrate a hash collision. Provide evidence, detail, and a basic algorithmic understanding of how the collision occurred by providing a detailed write up including appropriate diagrams, screenshots, and any other necessary visual aids (50 points).

- I attempted to use your hash.py program.  wasn't sure exactly what else to do after i manually attempted to calculate the text i entered `Decrypt me, I am secret!!!`.

    http://cl.xytify.net/cgi-bin/hash.py


    Results for: Decrypt me, I am secret!!!
    MD5: e1e6e36ab6e52efebb4435682e7dc416
    SHA-1: eca2ef310dd4c693aceacd5606533ee885f87caf
    SHA-256: 79ec8052a13eddfffb8a9abf9030d7581c783bdbcbe6b400170e4e603af20b82
    SHA-384: 2d28a34210847d122b7f7711e5ef252c16ca463990991c063ceaf9da00bc50a118f4b2b6ea3b30e8edbae8fa8364e4d3
    SHA-512: 2906638a0824d1cb54b3c1e0f1cfa7def6411183b732aa22e712bdd76f185a5637a250177d842c9e84034b75d9606abc1513cd90fb33c28d74cf715c4b1ecd1e

    ![alt text](<Screenshot 2024-11-01 at 1.55.40 PM.png>)


- Since I am visual I wanted to create my own python script using the same text `Decrypt me, I am secret!!!` and then modifying the text by adding a space at the end `Decrypt me, I am secret!!! `.  

    1. Imports:
        - Used Python’s built-in hashlib library, which provides hash functions, including MD5.
    2. Function: test_for_collision():
        - This function defines two inputs:
            - input1 is the original string: "Decrypt me, I am secret!!!".
            - input2 is a slightly modified version with an extra space at the end: "Decrypt me, I am secret!!! ".
        - Both inputs are encoded to bytes, as required by the hashlib.md5() function.
        - The function calculates the MD5 hash of each input using hashlib.md5(input).hexdigest(), which returns the hash in hexadecimal format.
        - It prints each input string and its respective MD5 hash.
        - The function then checks if the two MD5 hashes are identical:
            - If they match, it indicates an MD5 collision, prints a message confirming this, and returns True.
            - If they do not match, it prints a message stating no collision was found and returns False.
    3. Function: main():
        This function orchestrates the testing process, running test_for_collision() up to 50 times.
        It keeps track of whether a collision has been found, initializing collision_found to False.
        For each attempt, it prints the current attempt number, calls test_for_collision(), and checks if it returned True.
        If a collision is detected (True), the loop breaks immediately, indicating success.
        If the loop completes all 50 attempts without finding a collision, it prints a summary message indicating no collision was detected after 50 attempts.
    4. Execution:
        The script includes a conditional if __name__ == "__main__": block, which ensures the main() function only runs if the script is executed directly.

    Result:

    ![alt text](<Screenshot 2024-11-01 at 2.59.08 PM.png>)


- Summary, 

    Wasn't sure exactly how to perform this task.  I just remember doing a similary project in python in Python Security Programming with Prof. Logher. I know i deviated from using your python program but just decided to create a quick script to run up to 50 attempts if a collision had not been found before stopping the program. 



<br>

# Task 2:   Generate your own nested steganographic solution. It must include some secondary authentication mechanic. Provide the base message, the cover file, and methodology as a detailed write up (50 points).

1. Installed `OpenStego_0.8.60-1_all.deb` on my Ubuntu GCP instance.  

    - Installed OpenStego:

        ![alt text](<Screenshot 2024-11-01 at 11.34.18 AM.png>)

    - Installed Java:

        ![alt text](<Screenshot 2024-11-01 at 11.35.45 AM.png>)

    - Installed the OpenStego .deb package using dpkg

        ![alt text](<Screenshot 2024-11-01 at 11.34.51 AM.png>)


2. Text File prep and locating the cover image.

    - Created a text file namedd `EnlistedOath.txt`.

    - Copy/Pasted in the text file the Enlisted Oath, The Sailor's Creed, and the Navy Song - Anchors Aweigh.
    
        - Source: https://www.navy.mil/About/Our-Heritage/


3. We can start the process to embed/hide the file using OpenStego

    ![alt text](<Screenshot 2024-11-01 at 11.24.24 AM.png>)


    - Message File: I uploaded the text file I created.

    - Cover File:   I used a downloaded image of a VFA-103 SuperHornet fighter jet I used to maintain back from my Navy days.

        ![alt text](VFA103.jpeg)

    - Output Stego File:    Provided the file path to save my output file.  This is the updated file with the cover image listed with the text file hidden in the image.  
    
       ![alt text](<Screenshot 2024-11-01 at 12.28.55 PM.png>)


4. Extracting the Hidden File

    - enter the stego file:

        ![alt text](<Screenshot 2024-11-01 at 11.28.20 AM.png>)

    - Select the output folder:

       ![alt text](<Screenshot 2024-11-01 at 11.28.40 AM.png>)

    - Enter the password:   ^YHN6yhn

        ![alt text](<Screenshot 2024-11-01 at 11.29.17 AM.png>)


Summary:

    This was a nice exercise.  Although, as I was performing this task, I wasn't sure what you meant by `It must include some secondary authentication mechanic.`.  I didn't see there being an option to add  secondary authentication.  

<br>

# Task 3:  Sign your name on the list at dfw.xytify.net by hashing the value at dfw.xytify.net/hash.txt, ssh'ing in to the machine, and editing the file named editme. The password is also the username. If you need a hint, the combo is used in the Oath of Office taken by United States government officials (50 points).

So in this task i was completely lost in how to navigate resolving this.   I was unable to resolve this task. 

I wasn't sure if I had to break the hash using hashcat or a different program.   In total i just couldn't figure out what i had to do.   
