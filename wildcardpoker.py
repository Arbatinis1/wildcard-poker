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
    print(f"[+] Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    with open(output_file, "w") as f:
        f.write(result.stdout)
    if os.path.getsize(output_file) == 0:
        print(f"{RED}[ERROR] Command produced no output: {command}{RESET}")
    else:
        print(f"[✔] Output saved to {output_file}")

def run_nuclei(input_file, output_file):
    pass
