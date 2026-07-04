#!/bin/bash

# Clear terminal screen
clear

# Color codes for output styling
GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

echo -e "${YELLOW}[*] Updating system repositories...${RESET}"
# Update package list and upgrade existing packages
apt update -y && apt upgrade -y

echo -e "\n${YELLOW}[*] Installing required Python libraries...${RESET}"
# Install necessary Python dependencies used in the tool
pip install requests python-whois

echo -e "\n${GREEN}[+] All requirements installed successfully!${RESET}"
echo -e "${GREEN}[+] You can now run the tool using: python dark_hunter.py${RESET}"
