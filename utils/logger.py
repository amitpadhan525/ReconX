"""
Logging utilities for ReconX with ANSI color formatting.
"""

import sys
from datetime import datetime

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

def info(msg: str):
    print(f"{Colors.BLUE}[*]{Colors.RESET} {msg}")

def success(msg: str):
    print(f"{Colors.GREEN}[+]{Colors.RESET} {msg}")

def warn(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")

def error(msg: str):
    print(f"{Colors.RED}[-]{Colors.RESET} {msg}", file=sys.stderr)

def banner_header():
    art = f"""{Colors.CYAN}{Colors.BOLD}
  ____                     __  __
 |  _ \\ ___  ___ ___  _ __ \\ \\/ /
 | |_) / _ \\/ __/ _ \\| '_ \\ \\  / 
 |  _ <  __/ (_| (_) | | | |/  \\ 
 |_| \\_\\___|\\___\\___/|_| |_/_/\\_\\
{Colors.GRAY}      Modular Network Recon Tool{Colors.RESET}
"""
    print(art)
