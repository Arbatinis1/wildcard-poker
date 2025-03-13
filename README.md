Wildcard Subdomain Scanner
Wildcard Subdomain Scanner is a Python-based tool that automates subdomain discovery and vulnerability scanning. It combines powerful tools like Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei to streamline reconnaissance and security testing.

Features
Subdomain Enumeration: Discovers subdomains using Subfinder and Assetfinder.

HTTP Response Analysis: Collects status codes and response details for discovered subdomains using HTTPX.

Subdomain Takeover Detection: Identifies vulnerabilities with Subzy and Nuclei.

Organized Output: Saves results into structured files for analysis.

Installation
1.Clone this respitory:
git clone https://github.com/Arbatinis1/wildcard-poker.git
cd wildcard-poker
run python3 install.py this will install all required tools and dependencies to run this script

2.Install Python dependencies:
pip install -r requirements.txt

Usage
Usage
Run the script by executing the following command:

bash
python3 wildcardpoker.py
The script will:

Check and install missing dependencies.

Prompt you to enter a target domain (e.g., example.com).

Optionally create a folder to save output files.

Automatically run Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei to perform discovery and scanning tasks.

Output Files
After running, the script will generate the following files:

subfinder_output.txt: Results from Subfinder.

assetfinder_output.txt: Results from Assetfinder.

merged_subdomains.txt: Merged and cleaned list of subdomains.

httpx_results.txt: HTTP responses for discovered subdomains.

subzy_vulnerable.txt: Subdomains vulnerable to takeover (detected by Subzy).

nuclei_results.txt: Vulnerabilities detected by Nuclei.
