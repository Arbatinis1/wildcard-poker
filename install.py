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

def run_command(command):
    """Run a command and show output in real-time."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())
    process.wait()
    if process.returncode != 0:
        console.print(f"{RED}[ERROR]{RESET} Command failed: {command}")

def install_dependencies():
    """Install necessary dependencies."""
    console.print("[cyan][*] Installing dependencies...[/cyan]")
    subprocess.run("pip install rich", shell=True)
    subprocess.run("go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest", shell=True)
    subprocess.run("go install github.com/tomnomnom/assetfinder@latest", shell=True)
    subprocess.run("go install github.com/projectdiscovery/httpx/cmd/httpx@latest", shell=True)
    subprocess.run("go install github.com/LukaSikic/subzy@latest", shell=True)
    console.print("[green][✔] Installation complete![/green]")
    
    # Create main script
    create_main_script()

def create_main_script():
    """Generate the main script file."""
    script_content = """import os
import subprocess
import sys
from rich.console import Console

console = Console()

def run_command(command):
    """Run a command and show output in real-time."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())
    process.wait()

def main():
    console.print("[cyan][*] Starting Wildcard Poker Scanner...[/cyan]\n")
    target_domain = input("Enter the target domain to scan (e.g., example.com): ").strip()
    if not target_domain:
        console.print("[red][ERROR] No domain provided. Exiting...[/red]")
        sys.exit(1)
    project_folder = "WildcardPoker_Project"
    os.makedirs(project_folder, exist_ok=True)
    
    run_command(f"subfinder -d {target_domain} -all | tee {project_folder}/subfinder_output.txt")
    run_command(f"assetfinder --subs-only {target_domain} | tee {project_folder}/assetfinder_output.txt")
    merged_output = os.path.join(project_folder, "merged_subdomains.txt")
    with open(merged_output, "w") as merged_file:
        for filename in ["subfinder_output.txt", "assetfinder_output.txt"]:
            with open(os.path.join(project_folder, filename), "r") as f:
                merged_file.writelines(f.readlines())
    console.print("[green][✔] Merged subdomains saved to", merged_output)
    run_command(f"httpx -l {merged_output} -silent -status-code | tee {project_folder}/httpx_results.txt")
    run_command(f"subzy run --targets {merged_output} | tee {project_folder}/subzy_vulnerable.txt")
    console.print("[green][✔] Scan complete! Results saved in the project folder.[/green]")

if __name__ == "__main__":
    main()
    """
    with open("wildcardpoker.py", "w") as script_file:
        script_file.write(script_content)
    console.print("[green][✔] Created wildcardpoker.py script! You can now run 'python3 wildcardpoker.py' to use the tool.[/green]")

def main():
    console.print(LOGO)
    install_dependencies()
    console.print("[green][✔] Installation and setup complete! You can now run 'python3 wildcardpoker.py' to start scanning.")

if __name__ == "__main__":
    main()
