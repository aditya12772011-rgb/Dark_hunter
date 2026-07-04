import sys
import os
import requests
import socket
import whois

# ANSI Color Codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

# 1. Clear Screen
os.system('clear')

# 2. Banner
print(f"{YELLOW}-----------------------------------{RESET}")
print(f"{YELLOW}[+] STATUS: {RED}DARK HUNTER{RESET}")
print(f"{YELLOW}-----------------------------------{RESET}")

# 3. Input
url = input(f"{YELLOW}Enter URL:: {RESET}").strip()

print(f"\n{CYAN}[*] Target URL: {url}{RESET}")
print(f"{CYAN}[*] Checking website status, please wait...{RESET}\n")

try:
    domain_name = url.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
    response = requests.get(url, timeout=5)
    headers = response.headers
    
    if response.status_code == 200:
        print(f"{GREEN}[+] HTTP Status Code: {response.status_code}{RESET}")
        print(f"{GREEN}[+] Success: Website is Live!{RESET}\n")
        
        # --- FEATURE 1: IP ADDRESS DETECTOR ---
        print(f"{YELLOW}--------- TARGET NETWORK INFO ---------{RESET}")
        try:
            ip_address = socket.gethostbyname(domain_name)
            print(f"{GREEN}[+] IP: {YELLOW}{ip_address}{RESET}")
        except socket.gaierror:
            print(f"{RED}[-] Could not resolve IP Address.{RESET}")
            ip_address = None
        print(f"{YELLOW}---------------------------------------{RESET}\n")
        
        # --- FEATURE 2: REVERSE IP LOOKUP (NEW) ---
        print(f"{YELLOW}--------- REVERSE IP LOOKUP ---------{RESET}")
        if ip_address:
            print(f"{CYAN}[*] Finding other sites hosted on this IP...{RESET}")
            try:
                # Hackertarget को सार्वजनिक र निःशुल्क API प्रयोग गरेर होस्ट गरिएका साइट खोज्ने
                lookup_url = f"https://api.hackertarget.com/reverseiplookup/?q={ip_address}"
                lookup_res = requests.get(lookup_url, timeout=5)
                if "error" not in lookup_res.text.lower() and lookup_res.text:
                    sites = lookup_res.text.split('\n')
                    print(f"{GREEN}[+] Found {len(sites)} other domains on this server:{RESET}")
                    # सुरुका ५ वटा मात्र मुख्य डोमेनहरू देखाउने ता कि स्क्रिन फोहोर नहोस्
                    for site in sites[:5]:
                        print(f"    -> {site}")
                    if len(sites) > 5:
                        print(f"    ... and {len(sites)-5} more sites.")
                else:
                    print(f"{RED}[-] No other domains found or API limit reached.{RESET}")
            except Exception:
                print(f"{RED}[-] Failed to fetch Reverse IP data.{RESET}")
        else:
            print(f"{RED}[-] Cannot perform Reverse IP without IP address.{RESET}")
        print(f"{YELLOW}-------------------------------------{RESET}\n")

        # --- FEATURE 3: ROBOTS.TXT SCANNER (NEW) ---
        print(f"{YELLOW}--------- ROBOTS.TXT CRAWLER ---------{RESET}")
        print(f"{CYAN}[*] Checking for robots.txt...{RESET}")
        robots_url = f"https://{domain_name}/robots.txt"
        try:
            robots_res = requests.get(robots_url, timeout=5)
            if robots_res.status_code == 200:
                print(f"{GREEN}[+] Robots.txt found!{RESET}")
                # केवल 'Disallow' गरिएका संवेदनशील बाटोहरू मात्र छानेर देखाउने
                disallowed_paths = [line for line in robots_res.text.split('\n') if "disallow" in line.lower()]
                if disallowed_paths:
                    print(f"{YELLOW}[!] Hidden/Disallowed paths found:{RESET}")
                    for path in disallowed_paths[:5]: # सुरुका ५ वटा मात्र देखाउने
                        print(f"    {path}")
                else:
                    print(f"{YELLOW}[-] No Disallow rules specified in robots.txt.{RESET}")
            else:
                print(f"{RED}[-] Robots.txt not found on this website (Status: {robots_res.status_code}){RESET}")
        except Exception:
            print(f"{RED}[-] Failed to scan robots.txt{RESET}")
        print(f"{YELLOW}--------------------------------------{RESET}\n")
        
        # --- FEATURE 4: PORT SCANNER ---
        print(f"{YELLOW}--------- PORT SCANNER (DETAILED) ---------{RESET}")
        print(f"{CYAN}[*] Scanning common ports...{RESET}")
        ports_to_scan = [21, 22, 53, 80, 443, 8080]
        if ip_address:
            for port in ports_to_scan:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    print(f"{GREEN}[+] Port {port:<5} : OPEN{RESET}")
                else:
                    print(f"{RED}[-] Port {port:<5} : CLOSED{RESET}")
                s.close()
        print(f"{YELLOW}-------------------------------------------{RESET}\n")
        
        # --- FEATURE 5: WHOIS EMAIL EXTRACTOR ---
        print(f"{YELLOW}--------- PUBLIC EMAILS (WHOIS) ---------{RESET}")
        try:
            domain_info = whois.whois(domain_name)
            emails = domain_info.emails
            if emails:
                if isinstance(emails, list):
                    for email in set(emails):
                        print(f"{GREEN}[+] Found Email: {RESET}{email}")
                else:
                    print(f"{GREEN}[+] Found Email: {RESET}{emails}")
            else:
                print(f"{RED}[-] No public emails found.{RESET}")
        except Exception:
            print(f"{RED}[-] Failed to fetch WHOIS data.{RESET}")
        print(f"{YELLOW}-----------------------------------------{RESET}\n")
        
        # --- FEATURE 6: FIREWALL DETECTION (WAF) ---
        print(f"{YELLOW}--------- FIREWALL DETECTION ---------{RESET}")
        waf_detected = False
        if 'Server' in headers and 'cloudflare' in headers['Server'].lower():
            print(f"{GREEN}[+] Firewall Found: Cloudflare WAF{RESET}")
            waf_detected = True
        elif 'cf-ray' in headers:
            print(f"{GREEN}[+] Firewall Found: Cloudflare WAF{RESET}")
            waf_detected = True
        if not waf_detected:
            print(f"{YELLOW}[-] No obvious Firewall/WAF detected.{RESET}")
        print(f"{YELLOW}--------------------------------------{RESET}")
        
    else:
        print(f"{RED}[-] Website returned a non-200 code: {response.status_code}{RESET}")

except requests.exceptions.RequestException:
    print(f"{RED}[-] Error: Cannot connect to the website.{RESET}")
  
