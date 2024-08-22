

# Lab Setup

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


2. 