# Dark_hunter
DARK HUNTER — Advanced Reconnaissance Tool DARK HUNTER is an automated, command-line information gathering and reconnaissance tool developed in Python. Designed for security analysts and network administrators, it streamlines the initial phase of penetration testing by safely identifying active services, footprints, and potential entry. 

Key Features
Live Status & IP Resolution: Instantly checks if the target website is online and maps its domain name to the correct IPv4 address.
Detailed Port Scanner: Checks the status of the most common network ports and displays whether they are OPEN or CLOSED using clean, color-coded outputs.
HTTP Methods Auditing: Tests which request methods (GET, POST, OPTIONS, HEAD) are allowed by the web server to detect potential misconfigurations.
OSINT Intelligence: Performs a Reverse IP Lookup to discover other domains hosted on the same server and crawls the Robots.txt file to extract hidden paths and restricted directories.
WHOIS Email & WAF Detection: Extracts public registration contact emails and inspects HTTP headers to identify active Web Application Firewalls (WAF) like Cloudflare.
How to Use
To run DARK HUNTER on your Linux terminal or Termux environment, follow these three simple steps:
Step 1: Install Dependencies
Give execution permissions to the setup script and run it to automatically install all required packages and Python libraries:

chmod +x setup.sh && ./setup.sh

Step 2: Run the Tool
Once the setup is complete, launch the main script using Python:
python dark_hunter.py

Step 3: Enter Target URL
When prompted with Enter URL::, type the full address of the target website (e.g., https://example.com) and hit enter. The tool will display all gathered information sequentially within seconds.
