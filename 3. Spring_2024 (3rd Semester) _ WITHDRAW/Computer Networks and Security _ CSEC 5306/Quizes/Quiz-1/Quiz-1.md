Ruben Valdez <br />
CSEC 5306 | Computer Networks and Security <br />
Prof. Alsmadi <br />
Quiz 1: Crypto Lab -- Secret-Key Encryption

<br />

# SEED Lab Environment Setup

1. Created a GCP Instance to host the SEED Lab environment.

   ![alt text](<Screenshot 2024-02-11 at 9.07.51 PM.png>)

2. Generated SSH Keys on my physical Apple M1 machine using Terminal and add the .pub key to the GCP metadata so I can SSH into my GCP instance using Terminal.

   ![alt text](<Screenshot 2024-02-11 at 9.11.03 PM.png>)

3. Successful SSH logon to the `netsec-5306` instance.

   ![alt text](<Screenshot 2024-02-11 at 9.12.24 PM.png>)

4. Added `RValdez` as a user and added it to the sudoers list.

   ![alt text](<Screenshot 2024-02-11 at 9.14.52 PM.png>)

   ![alt text](<Screenshot 2024-02-11 at 9.16.13 PM.png>)

5. Performed simple directory folder creation

   ![alt text](<Screenshot 2024-02-11 at 9.21.02 PM.png>)

<br/>
<br/>

# Crypto Lab Setup

1. Download the Crypto Lab -- Secret-Key Encryption `Labsetup.zip` file:
   
   ![alt text](<Screenshot 2024-02-11 at 9.22.17 PM.png>)


2. Installed `unzip` to unzip the contents.

   ![alt text](<Screenshot 2024-02-11 at 9.23.41 PM.png>)

   ![alt text](<Screenshot 2024-02-11 at 9.26.30 PM.png>)


3. 


4. 


5. 


# Task 1: Frequency Analysis

<br>
Completed Steps 1-3:

1. Created a python script named `keygen.py`

   ![alt text](<Screenshot 2024-02-12 at 9.44.30 AM.png>)


2. Created the following file `article.txt` and converted all upper cases to lower cases, and then removed all the punctuations and numbers.

   - `artical.txt` initial text
   
      ![alt text](<Screenshot 2024-02-12 at 9.51.10 AM.png>)

   - Commands to convert creating a new text file `lowercase.txt`

      ![alt text](<Screenshot 2024-02-12 at 9.49.08 AM.png>)

   - `lowercase.txt` conversion

      ![alt text](<Screenshot 2024-02-12 at 9.55.57 AM.png>)


3. Used the tr command to do the encryption.

   - Conversion to cipher.

      ![alt text](<Screenshot 2024-02-12 at 11.32.57 AM.png>)

   - `ciphertext.txt`
      
      ![alt text](<Screenshot 2024-02-12 at 11.30.51 AM.png>)

Example, replaced letters a, e, and t in in.txt with letters X, G, E and the results are saved in out.txt.

   ![alt text](<Screenshot 2024-02-12 at 12.55.57 PM.png>)

   ![alt text](<Screenshot 2024-02-12 at 12.56.28 PM.png>)


<br>

# Task 2: Encryption using Different Ciphers and Modes

<br>

Using `openssl`, encrypting `article.txt` file with three separate encryption types:

- aes-128-ebc
- aes-128-ecb
- aes-256-ecb 

   ![alt text](<Screenshot 2024-02-12 at 1.40.43 PM.png>)

Using `openssl`, decrypting each file:

- cipher1.bin
- cipher2.bin
- cipher3.bin

   ![alt text](<Screenshot 2024-02-12 at 2.09.59 PM.png>)


<br>

# Task 3: Encryption Mode – ECB vs. CBC

<br>

1. Encrypting `pic_orginal.bmp` using ECB and CBC.

   ![alt text](<Screenshot 2024-02-12 at 3.42.50 PM.png>)

2. Unable to view `comb_cbc.bmp` or `comb_ecb.bmp` file after installing `eog`.

   - Since I was predominately using SSH from my Mac M1 Silicon Terminal, I was unable to successfully open the file.  

      ![alt text](<Screenshot 2024-02-12 at 4.14.35 PM.png>)

   - Another attempt was accessing a GUI environment by RDP using `Chrome Remote Desktop`.
      
      ![alt text](<Screenshot 2024-02-12 at 4.11.22 PM.png>)


<br>

# Task 4: Padding

<br>

1. `f1.txt - f3.txt` files created.

   ![alt text](<Screenshot 2024-02-12 at 4.54.32 PM.png>)

2. Encrypting using the following cipher modes:
   
   - ECB

      ![alt text](<Screenshot 2024-02-12 at 5.16.05 PM.png>)

   - CBC
   
      ![alt text](<Screenshot 2024-02-12 at 4.58.57 PM.png>)

   - CFB

      ![alt text](<Screenshot 2024-02-12 at 5.16.31 PM.png>)

   - OFB

      ![alt text](<Screenshot 2024-02-12 at 5.17.26 PM.png>)


3. Decrypting the following files:

   - List of encrypted files to pick from to decrypt:
   
      ![alt text](<Screenshot 2024-02-12 at 5.22.07 PM.png>)
   
   - Decrypted one of each cipher mode from the list above. 

      ![alt text](<Screenshot 2024-02-12 at 5.45.16 PM.png>)


# Task 5: Error Propagation – Corrupted Cipher Text

1. Created a python script `task5.py` that creates a text file with 1000 bytes long.

   ![alt text](<Screenshot 2024-02-12 at 7.33.35 PM.png>)

2. Encrypt the file `task5.txt`


3. Unable to use `Bless` it just continues to crash leaving me unable to perform any further file analysis.  

   - Instead of `Bless`, I just ran `sha1sum` to calculate the checksum and hash.  Based off the output of each file, it doesn't appear to show any difference or changes between the two files.
      
      ![alt text](<Screenshot 2024-02-12 at 8.36.42 PM.png>)


# Task 6: Initial Vector (IV) and Common Mistakes

## Task 6.1. IV Experiment

Created 3 encrypted files:

![alt text](<Screenshot 2024-02-12 at 9.20.19 PM.png>)

Compared 1 and 2, then 2 and 3 files using `diff -q <file> <file>`.  The `-q` option only verifies if the files are different.

![alt text](<Screenshot 2024-02-12 at 9.17.04 PM.png>)

## Task 6.2. Common Mistake: Use the Same IV

- Generated plaintext > ciphertext keys

   ![alt text](<Screenshot 2024-02-12 at 10.28.18 PM.png>)

- Generated the encodings and then decrypted the message for P2.

   ![alt text](<Screenshot 2024-02-12 at 10.27.43 PM.png>)

Note: Unable to figure out the python code to determine the outcome. 



