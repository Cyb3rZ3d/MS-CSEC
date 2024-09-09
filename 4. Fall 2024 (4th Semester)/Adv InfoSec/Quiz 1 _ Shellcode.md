

# Google Cloud Platform (GCP) SEED 2.0 Ubuntu Lab Setup

1. GCP instance build and firewalls

    - Created a Google Cloud Platform (GCP) Ubuntu Instance using the SEED VM GitHub instructions

        `https://github.com/seed-labs/seed-labs/blob/master/manuals/cloud/create_vm_gcp.md`

        ![alt text](<Screenshot 2024-08-21 at 11.39.56 AM.png>)


    - Using my local system I created the SSH Key Generation

        ![alt text](<Screenshot 2024-08-21 at 10.34.37 AM.png>)


    - I modified the SSH .pub key to add the GCP username and the instance external IP address

        ![alt text](<Screenshot 2024-08-21 at 10.41.18 AM.png>)


   - In GCP, I added the .pub key to GCP's Metadata to store the key so I can remotely SSH into my Ubuntu instance.

        ![alt text](<Screenshot 2024-08-21 at 10.48.21 AM.png>)


    - Connect to the GCP Ubuntu instance using SSH.

        ![alt text](<Screenshot 2024-08-21 at 10.57.30 AM.png>)


    - Created firewall rules for SSH and VNC

        ![alt text](<Screenshot 2024-08-21 at 11.26.13 AM.png>)


2. Installed the software and configured the instance for labs.

    ![alt text](<Screenshot 2024-08-21 at 12.07.39 PM.png>)

    ![alt text](<Screenshot 2024-08-21 at 12.08.21 PM.png>)

    ![alt text](<Screenshot 2024-08-21 at 12.09.00 PM.png>)



    ![alt text](<Screenshot 2024-08-21 at 12.26.36 PM.png>)
    
    
    Installed `Chrome Remote Desktop` using the following instructions


    
    ![alt text](<Screenshot 2024-08-21 at 3.51.12 PM.png>)


# Shellcode Lab

1. Created a new directory for the Shellcode lab and downloaded the zip file `Labsetup.zip` and unziped it to obtain the required files.  The following are commands used to create a directory, download a zip file, and unzip the file.

    ![alt text](<Screenshot 2024-08-27 at 12.50.53 PM.png>)


## Task 1

1. Samlple of `hello.s` amd64 assembly program

    ![alt text](<Screenshot 2024-08-27 at 7.45.23 PM.png>)


2. Compiling assembly code to object code and linking to generate final binary

    ![alt text](<Screenshot 2024-08-27 at 7.42.29 PM.png>)


3. Extracting machine code (shellcode) from a executable using `objdump` to disassemble the object file or executable using the command `objdump -Mintel -d hello.o`.

    ![alt text](<Screenshot 2024-08-27 at 7.59.02 PM.png>)


4. Used the command `xxd -p -c 20 hello.o` to print out the binary of the machine code

    ![alt text](<Screenshot 2024-08-27 at 8.08.08 PM.png>)


## Task 2: Writing Shellcode (Approach 1)

### Task 2.a. Understand the code

