# wildcard-poker
Wildcard Subdomain Scanner automates subdomain discovery and vulnerability scanning using tools like Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei.
Wildcard Subdomain Scanner
The Wildcard Subdomain Scanner is a Python-based automation tool that combines several powerful tools to streamline the reconnaissance and vulnerability scanning process. It automates subdomain discovery, HTTP response collection, and subdomain takeover detection using tools like Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei.

Features
Subdomain Enumeration:

Combines the output of Subfinder and Assetfinder to discover subdomains of a target domain.

HTTP Response Analysis:

Uses HTTPX to collect status codes and response details for discovered subdomains.

Subdomain Takeover Detection:

Integrates Subzy and Nuclei to identify potentially vulnerable subdomains.

Customizable Output:

Saves results to organized text files for later analysis.

Dependency Checks:

Ensures that all required tools and libraries are installed before running the script.

How It Works
Prerequisites Check:

The script verifies that the required Python libraries (rich) are installed.

Checks for the Go programming language, which is necessary for tools like Subfinder and Assetfinder.

Verifies the presence of external tools: Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei.

If dependencies are missing, the script guides the user on installing them.

Subdomain Enumeration:

Runs Subfinder and Assetfinder to find subdomains of the specified domain.

Merges and cleans the results to remove duplicates and invalid entries.

HTTPX Response Gathering:

Uses HTTPX to collect response status codes for the discovered subdomains, helping to identify live domains.

Subdomain Takeover Detection:

Executes Subzy to detect potential subdomain takeovers.

Uses Nuclei with takeover-specific templates to detect further vulnerabilities.

Organized Output:

Outputs results to well-structured files:

merged_subdomains.txt: All discovered subdomains.

httpx_results.txt: Subdomains with HTTP response details.

subzy_vulnerable.txt: Subdomains vulnerable to takeover (identified by Subzy).

nuclei_results.txt: Vulnerabilities detected by Nuclei.

Installation Instructions
To set up and run this script, follow these steps:

Clone this repository:

bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Install Python dependencies:

bash
pip install -r requirements.txt
Ensure the following tools are installed and available in your system's PATH:

Subfinder: Installation Instructions

Assetfinder: Installation Instructions

HTTPX: Installation Instructions

Subzy: Installation Instructions

Nuclei: Installation Instructions

Ensure the Go programming language is installed:

Download and Install Go

Run the script:

bash
python wildcard.py
Usage Instructions
When you run the script, it will:

Check and install missing dependencies.

Prompt you to enter a target domain (e.g., example.com).

Optionally create a folder for project organization.

Automatically run Subfinder, Assetfinder, HTTPX, Subzy, and Nuclei.

Outputs will be saved in the specified project folder:

subfinder_output.txt: Subfinder results.

assetfinder_output.txt: Assetfinder results.

merged_subdomains.txt: Combined and cleaned subdomains list.

httpx_results.txt: HTTPX responses.

subzy_vulnerable.txt: Subdomains vulnerable to takeover (Subzy).

nuclei_results.txt: Vulnerabilities detected by Nuclei.

Example workflow:

Enter example.com as the target domain.

Let the script discover subdomains, gather HTTP responses, and scan for vulnerabilities.

Review the output files in the project folder.

Example Commands (Advanced Users)
To manually use the tools integrated into the script:

Subfinder:

bash
subfinder -d example.com -all
Assetfinder:

bash
assetfinder --subs-only example.com
HTTPX:

bash
httpx -l merged_subdomains.txt -silent -status-code
Subzy:

bash
subzy run --targets merged_subdomains.txt
Nuclei:

bash
nuclei -l merged_subdomains.txt -t takeover -o nuclei_results.txt
Notes for Users
Ensure that the required tools and libraries are installed before running the script.

If you encounter issues, verify that all tools are updated to their latest versions.

The script is optimized for security researchers and penetration testers but should be used responsibly and with proper authorization.
