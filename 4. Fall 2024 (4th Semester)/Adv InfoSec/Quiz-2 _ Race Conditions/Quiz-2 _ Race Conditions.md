Ruben Valdez <br>
CSEC 5327 _ Advanced InfoSec <br>
Prof. Dr. Alsmadi <br>
Quiz-2 _ Race Conditions
Due: Sept. 15
==========================

<br>

# Lab Setup

- Using the GUI for Ubuntu I created a new folder `Quiz-2 _ RaceConditions`

    ![alt text](<Screenshot 2024-09-09 at 10.11.35 AM.png>)


- Using Terminal I downloaded the Race Conditions zip file
    
    `curl -o src-cloud.zip https://seedsecuritylabs.org/Labs_20.04/Files/Race_Condition/Labsetup.zip`


- Unziped the folder

    `unzip src-cloud.zip`

    ![alt text](<Screenshot 2024-09-09 at 10.07.32 AM.png>)


<br>

# Environment Setup

- Turning off countermeasures

    ```
    sudo sysctl -w fs.protected_symlinks=0

    sudo sysctl fs.protected_regular=0
    ```

    ![alt text](<Screenshot 2024-09-09 at 1.27.31 PM.png>)


- Reviewing of the Vulnerable Program, `vulp.c`, containing the Race Condition vulnerability

    ![alt text](<Screenshot 2024-09-09 at 2.05.51 PM.png>)


- After reviewing the code in the `vulp.c` program we can proceed with setting up the `Set-UID` program by doing the following steps

    1. Compile the `vulp.c` code 

    2. Turn the binary into a Set-UID program owned by root 

    3. Modify the file permissions so that the owner can read, write, and execute permissions; the group has read and executions permissions; and all others have read permissions.

    ```
    gcc vulp.c -o vulp
    sudo chown root vulp
    sudo chmod 4755 vulp
    ```

    - Before:

        ![alt text](<Screenshot 2024-09-09 at 2.32.40 PM.png>)

    - After:

        We can see the permission changes were completed with identifying the ownership of the file is now with `root`

        ![alt text](<Screenshot 2024-09-09 at 2.33.09 PM.png>)


<br>

# Task 1: Choosing Our Target

- Lets take a look at the `/etc/passwd` file and look at the user's, particularly the `root` user. We need to confirm the third field (the user ID field) is set to `0` confirming the process's the user ID field, and not necessarily the name `root`.

    `root:x:0:0:root:/root:/bin/bash`
    
    ![alt text](<Screenshot 2024-09-09 at 3.11.05 PM.png>)


- In this step, we add a user to the `/etc/passwd` file with the provided user credentials to add:

    `test:U6aMy0wojraho:0:0:test:/root:/bin/bash`

    Note: we can verify we see multiple recognizable user's such as root, seed, and my ubuntu account ruben.valdez0

    ![alt text](<Screenshot 2024-09-09 at 10.32.48 PM.png>)


- Testing the new user `test` logon, lets change the user account from `ruben.valdez0` to `test` using the following commands:

    ```
    su test

    Note:  When prompted for the password, press enter without entering the password.
    
    whoami
    ```

    We can now confirm the user `test` account is now a root user.

    ![alt text](<Screenshot 2024-09-09 at 10.42.26 PM.png>)

- Per the lab instruction, I deleted the user `test` and it's credentials from the `/etc/passwd` file.

    ![alt text](<Screenshot 2024-09-09 at 10.49.24 PM.png>)


<br>

# Task 2: Launching the Race Condition Attack

## Task 2.A: Simulating a Slow Machine

Let's open up a 10-second time window by exploiting the race condition in the `Set-UID` program.

- Modified the `vulp.c` code to include `sleep(10);`.

    ![alt text](<Screenshot 2024-09-09 at 10.54.17 PM.png>)

    ```
    ln -sf /dev/null /tmp/XYZ
    ls -ld /tmp/XYZ
    ````

    ![alt text](<Screenshot 2024-09-10 at 2.28.00 PM.png>)



# Summary

In summary, the Race Condition Vulnerability Lab encompasses the setup of the lab environment, tasks related to user management and permissions, and the execution of a race condition experiment using a symbolic link. The outcome of this experiment reveals that the symbolic link has permissive permissions, granting unrestricted read, write, and execution access to any user.