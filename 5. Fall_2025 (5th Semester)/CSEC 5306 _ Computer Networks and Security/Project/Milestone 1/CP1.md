***Ruben Valdez*** <br>
CSEC 5306 | Computer Networks & Security <br>
Prof. Alsmadi, Izzat <br>
Course Project - Mileston 1 <br>
Due: Feb. 17, 2025 <br>

---

# Instructions:

    This is the major course project and report
    
    In the first deliverable, you are expected to download (Network-Security-Analysis-master.zip), explain and produce a report of the code in this link that includes several network security analysis methods 
    
    Use examples of websites to demo the code and how it works

    Option2: Using any code project from the link below:

    https://github.com/search?q=%22network+security%22+language%3APython&type=repositories
    
    Due Feb. 15th

---

<br >
<br >

# Report on Web Vulnerability Scanner: `scanner.py`

***GitHub Source:***    https://github.com/Cyb3rZ3d/web-vulnerability-scanner

![alt text](<Screenshot 2024-02-15 at 8.00.23 PM.png>)

The application I chose for this first milestone is a custom web vulnerability scanner.  It was built using Python 3 and the name of the program is `scanner.py`.  Nothing too unique in the naming convention of this program but underneath the hood, this is a great program as it scans for Cross-Site Scripting (XSS), and Local File Inclusion (LFI).

Before diving into the program further, lets briefly define XSS and LFI: 

- LFI: is a type of vulnerability commonly found in web applications that allow an attacker to include files on the server by exploiting insecure file include mechanisms. This vulnerability typically arises when the web application includes files based on user input without proper validation, allowing an attacker to manipulate the input to include arbitrary files from the local file system.

- XXS: is a type of security vulnerability commonly found in web applications. It occurs when an attacker injects malicious scripts into web pages viewed by other users. These scripts can execute in the context of the victim's browser, leading to various consequences such as session hijacking, cookie theft, keylogging, or defacement of websites.  Three types of XSS attacks are as followed:

    - Stored XSS: The malicious script is permanently stored on the target server, such as in a database or message board. When other users access the affected web page, they inadvertently execute the injected script.

    - Reflected XSS: The injected script is reflected off the web server, typically as part of a URL or form input. The script is then executed in the victim's browser when they visit the manipulated URL or submit the form.
    
    - DOM-based XSS: Occurs when the vulnerability is in the client-side code rather than the server-side code. The malicious script is injected into the Document Object Model (DOM) of the web page and executed by the victim's browser when the page is loaded or manipulated dynamically.


<br >

## Lab Setup Steps:

Prior to beginning testing the web vulnerability program, we must setup out test enviroment.  The following are the step I took to complete the lab setup: 

- Using VMware Fusion, I installed Kali Linux 2023.4.

- Installed updates and upgrades to the Kali OS

- Installed VScode and all the needed Python extentions.

- cloned the github repository: git clone https://github.com/Mar0dev/web-vulnerability-scanner.git

    - Confirmed the files that were retrieved and downloaded by `cd web-vulnerability-scanner`
        
        - CLI view of the installed programs:

            ![alt text](<Screenshot 2024-02-15 at 10.14.14 PM.png>)

        - VScode folder side view of the installed programs:
            
            ![alt text](<Screenshot 2024-02-15 at 10.16.15 PM.png>)

- Completed a pip install, `pip install -r requirements.txt`

    ![alt text](<Screenshot 2024-02-15 at 10.22.25 PM.png>)

<br >

Now that we've completed the lab setup, we can now begin using the web vulnerability program.


## Example 1 - Scanning in Quite Mode and without HSTS header

- Accessing the help page `python3 ./scanner.py -h`

    ![alt text](<Screenshot 2024-02-15 at 8.00.23 PM.png>)

- Seleting the following options `-q` for quite mode and `-nh` for not checking for the http headers

    - Here we can see there was a HTTP code 200, indicating a the request was successful.  Another note, you can visibly see there were no further traffic here in the CLI.

        ![alt text](<Screenshot 2024-02-15 at 10.36.30 PM.png>)

    - After the scan was completed, the vulnerability scan results were then written to a file named `audit_20240215-2229`
        
        The file identifies an Nmap was completed, 

        ![alt text](<Screenshot 2024-02-15 at 10.41.56 PM.png>)



## Example 2 - Scanning with extended list of XSS paylos with crawler depth set to 3

This example was a dinger. After following the authors isntructions that was listed in this GitHub repository, the program was experiencing some issues and crashed in the middle of scanning.  The following are attempts I made to run the prescribed command and a few attempts using a different command but staying in line with the options that were first indicated:

1. `python3 ./scanner.py -u http://testphp.vulnweb.com -c 3 -xp ./payloads/xss_payloads_long.txt` 

    The program crashed after starting the scan.  It appear to have stopped during the check for XXS vulnerabilities.

    CLI command and scan:

    ![alt text](<Screenshot 2024-02-15 at 11.28.24 PM.png>)
    
    Audit File:

    ![alt text](<Screenshot 2024-02-15 at 11.27.11 PM.png>)

2. `python3 ./scanner.py -u http://testphp.vulnweb.com/guestbook.php -c 3 -xp ./payloads/xss_payloads_long.txt`

    Here I attempted to modify the url site and kept everything else the same and was unsuccessful as the same issues persisted.  The site would either freeze or crash when checking for XSS vulnerabilities.  

    CLI command and scan:

    ![alt text](<Screenshot 2024-02-15 at 11.23.38 PM.png>)

    Audit File:
    
    ![alt text](<Screenshot 2024-02-15 at 11.25.55 PM.png>)

3. `python3 ./scanner.py -u http://testphp.vulnweb.com/guestbook.php -c 3 -xp ./payloads/xss_payloads_short.txt`

    SUCCESS!!!  It appear that changing the text file from `xss_payloads_long.txt` to `xss_payloads_short.txt` was the trigger that allowed the program to start and finish successfully.   

    CLI command and scan:

    ![alt text](<Screenshot 2024-02-15 at 11.20.52 PM.png>)

    Audit File:
    ![alt text](<Screenshot 2024-02-15 at 11.21.34 PM.png>)


4. `python3 ./scanner.py -u http://testphp.vulnweb.com -c 3 -xp ./payloads/xss_payloads_short.txt`

    Just to further test the original URL for this example, I kept all the same option but instead used the `xss_payloads_short.txt` file.  This scan just like bullet # 3, was SUCCESSFUL!!!  It completed the scan and outputed a audit file `audit_20240215-2308`.

    CLI command and scan:

    ![alt text](<Screenshot 2024-02-15 at 11.13.50 PM.png>)

    Audit File:

    ![alt text](<Screenshot 2024-02-15 at 11.19.03 PM.png>)


## Quick Notes:

SQLi is error based

LFI detection works on PHP sites

# Summary

This tools was simple to use and straight forward. Although, there was a few dingers but after some troubleshooting and just selecting different text files seemed to work.  The option were used without any issues or complications.  Overall a quick assessment I would say this program was easy to understand and can be an proficient tool in the web vulnerability tools arsenal just to gather the details to crawl a website or even just a all in one program to test for XSS, LFI.  


<br >
<br >

# References

<br >

Nutting, R. (2019). Chapter 9: Web and Database Attacks, CompTIA PenTest+ Certification All-in-One Exam Guide (PT0-001) (pp. 251-253). McGraw-Hill Education.
These few pages refer to the difinitions to Local File Inclusion (LFI)

Nutting, R. (2019). Chapter 9: Web and Database Attacks, CompTIA PenTest+ Certification All-in-One Exam Guide (PT0-001) (pp. 261-262). McGraw-Hill Education.
These few pages refer to the difinitions to Local Cross-Site Scripting (XSS)
