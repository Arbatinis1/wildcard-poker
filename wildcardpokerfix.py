import os
import subprocess
import sys
import shutil
from rich.progress import Progress
from rich.console import Console
import time

# ANSI escape codes for terminal colors
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

console = Console()

LOGO = f"""{GREEN}

██╗    ██╗██╗██╗     ██████╗  ██████╗ █████╗ ██████╗ ██████╗     ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ 
██║    ██║██║██║     ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
██║ █╗ ██║██║██║     ██║  ██║██║     ███████║██████╔╝██║  ██║    ██████╔╝██║   ██║█████╔╝ █████╗  ██████╔╝
██║███╗██║██║██║     ██║  ██║██║     ██╔══██║██╔══██╗██║  ██║    ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
╚███╔███╔╝██║███████╗██████╔╝╚██████╗██║  ██║██║  ██║██████╔╝    ██║     ╚██████╔╝██║  ██╗███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝╚══════╝╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

{RESET}"""

def check_python_libraries():
    """Check and install missing Python libraries."""
    required_libraries = ["rich"]
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            console.print(f"{RED}[ERROR]{RESET} Missing Python library: {lib}. Installing it now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            console.print(f"{GREEN}[✔]{RESET} Installed: {lib}")

def check_go_installation():
    """Check if Go language is installed."""
    if not shutil.which("go"):
        console.print(f"{RED}[ERROR]{RESET} Go programming language is not installed.")
        console.print(f"{CYAN}Please install Go from https://golang.org/dl/ {RESET}")
        sys.exit(1)  # Exit script since Go is essential
    else:
        console.print(f"{GREEN}[✔]{RESET} Go programming language is installed.")

def check_external_tools():
    """Check if required external tools are installed."""
    tools = {
        "subfinder": "https://github.com/projectdiscovery/subfinder",
        "assetfinder": "https://github.com/tomnomnom/assetfinder",
        "httpx": "https://github.com/projectdiscovery/httpx",
        "subzy": "https://github.com/LukaSikic/subzy",
        "nuclei": "https://github.com/projectdiscovery/nuclei"
    }
    for tool, url in tools.items():
        if not shutil.which(tool):
            console.print(f"{RED}[ERROR]{RESET} Missing tool: {tool}. Please install it from {CYAN}{url}{RESET}.")

def loading_animation():
    with Progress() as progress:
        task = progress.add_task("[cyan]Initializing...", total=100)
        for i in range(100):
            time.sleep(0.05)
            progress.update(task, advance=1)
        console.print("[green][✔] Initialization complete![/green]")

def create_folder():
    create_new = input("Do you want to create a new project folder? (recommended) (y/n): ").strip().lower()
    if create_new == "y":
        folder_path = input("Enter the folder path (absolute or relative): ").strip()
        os.makedirs(folder_path, exist_ok=True)
        print(f"[✔] Folder created at: {folder_path}")
        return folder_path
    else:
        auto_folder = os.path.join(os.getcwd(), "WildcardPoker_Project")
        os.makedirs(auto_folder, exist_ok=True)
        print(f"[✔] Using default project folder: {auto_folder}")
        return auto_folder

def run_command(command, output_file):
    """Run a command and stream output to the terminal and save to a file."""
    print(f"[+] Running: {command}")
    
    with open(output_file, "w") as f:
        # Use subprocess to stream output in real-time
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            print(line, end="")  # Show in terminal
            f.write(line)        # Write to file
        for line in process.stderr:
            print(f"{RED}{line.strip()}{RESET}", end="")  # Show errors in terminal
        
    return_code = process.wait()
    if return_code != 0:
        print(f"{RED}[ERROR] Command failed with return code {return_code}: {command}{RESET}")
    else:
        print(f"{GREEN}[✔] Output saved to {output_file}{RESET}")

def run_nuclei(input_file, output_file):
    """Run Nuclei on the input file and save output."""
    command = f"nuclei -l {input_file} -o {output_file}"
    run_command(command, output_file)

def main():
    console.print(LOGO)
    console.print("[cyan][*] Starting Wildcard Subdomain Scanner...[/cyan]\n")

    # Step 1: Check for prerequisites
    console.print("[cyan][*] Checking prerequisites...[/cyan]")
    check_python_libraries()
    check_go_installation()
    check_external_tools()

    # Step 2: Get the target domain
    target_domain = input("Enter the target domain to scan (e.g., example.com): ").strip()
    if not target_domain:
        console.print(f"{RED}[ERROR]{RESET} No domain provided. Exiting...")
        sys.exit(1)

    # Step 3: Create project folder
    project_folder = create_folder()

    # Step 4: Run Subfinder
    subfinder_output = os.path.join(project_folder, "subfinder_output.txt")
    run_command(f"subfinder -d {target_domain} -all", subfinder_output)

    # Step 5: Run Assetfinder
    assetfinder_output = os.path.join(project_folder, "assetfinder_output.txt")
    run_command(f"assetfinder --subs-only {target_domain}", assetfinder_output)

    # Step 6: Combine results (merge subdomains)
    merged_output = os.path.join(project_folder, "merged_subdomains.txt")
    with open(merged_output, "w") as merged_file:
        with open(subfinder_output, "r") as sf_file, open(assetfinder_output, "r") as af_file:
            merged_file.writelines(set(sf_file.readlines() + af_file.readlines()))
    console.print(f"[green][✔]{RESET} Merged subdomains saved to {merged_output}")

    # Step 7: Run HTTPX
    httpx_output = os.path.join(project_folder, "httpx_results.txt")
    run_command(f"httpx -l {merged_output} -silent -status-code", httpx_output)

    # Step 8: Run Subzy
    subzy_output = os.path.join(project_folder, "subzy_vulnerable.txt")
    run_command(f"subzy run --targets {merged_output}", subzy_output)

    # Step 9: Run Nuclei
    nuclei_output = os.path.join(project_folder, "nuclei_results.txt")
    run_nuclei(merged_output, nuclei_output)

    console.print("[green][✔] Scan complete! All results are saved in the project folder.[/green]")

if __name__ == "__main__":
    main()
