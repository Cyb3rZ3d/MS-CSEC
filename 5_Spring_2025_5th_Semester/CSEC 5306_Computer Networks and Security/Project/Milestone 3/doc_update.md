

Abstract:
This project explores the development and enhancement of a lightweight Python-based web vulnerability scanner named scanner.py, designed to detect common security issues such as Cross-Site Scripting (XSS) and Local File Inclusion (LFI). The primary goal is to provide an intuitive, accessible tool for educational and small-scale security assessments. Throughout Milestones 1 and 2, the tool was tested, compared against open-source alternatives, and reviewed in the context of academic literature. In Milestone 3, enhancements were implemented to improve functionality, including report summarization, input form logging, and vulnerability counters. Experiments were conducted using varied payload sets and crawler depths to validate the scanner's detection capabilities and performance limitations. Findings revealed that while scanner.py lacks advanced features found in tools like OWASP ZAP and SecuBat, it remains a valuable educational utility. This report concludes by discussing the tool’s current capabilities, its limitations, and future directions for development, such as multithreading, structured output, and expanded vulnerability detection.


Intro:
Web applications are frequent targets of cyberattacks, making early detection of vulnerabilities crucial. Traditional scanners can be resource-intensive or complex for novice users. This project explores the design and implementation of a user-friendly, Python-based vulnerability scanner named scanner.py. The scanner focuses on detecting XSS and LFI vulnerabilities using payload injection and response analysis. This report presents the integrated outcomes of Milestones 1 and 2 and expands with experimental testing, literature insight, and scanner enhancements in Milestone 3.


Milestone 1: Scanner Overview and Lab Setup

Milestone 1 served as the foundational phase of this project, focused on understanding and deploying a custom-built Python web vulnerability scanner. The primary objectives were to establish a secure test environment and evaluate the tool's ability to detect Cross-Site Scripting (XSS) and Local File Inclusion (LFI) vulnerabilities. This milestone included the installation of required dependencies, setup of the virtual lab using Kali Linux, and running multiple scans against a known vulnerable site. The observations from this phase informed areas for future tool refinement and formed the groundwork for deeper analysis in subsequent milestones.

The scanner was tested using a controlled lab setup:
- Platform: Kali Linux 2023.4 on VMware Fusion
- Tool: scanner.py from the GitHub repository web-vulnerability-scanner
- Target Site: http://testphp.vulnweb.com

Experiments were conducted using both short and long XSS payloads with varied crawler depths. Observations included successful scans with short payloads and tool crashes with longer payload files, indicating performance limitations.



Milestone 2:




Milestone 3:




Conclusion:


References:


