"""
Helper functions for target resolution, port parsing, and results exporting.
"""

import json
import os
import socket
from typing import List, Optional

def parse_ports(port_input: str) -> List[int]:
    """
    Parses various port input specifications:
    - Single: '80'
    - Range: '1-1000'
    - List: '80,443,8080'
    - Mixed: '21,22,80-90,443'
    """
    ports = set()
    parts = port_input.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start, end = int(start_str.strip()), int(end_str.strip())
            if start > end:
                start, end = end, start
            for p in range(max(1, start), min(65535, end) + 1):
                ports.add(p)
        else:
            p = int(part)
            if 1 <= p <= 65535:
                ports.add(p)
    return sorted(list(ports))

def resolve_target(target: str) -> Optional[str]:
    """
    Resolves a hostname to an IP address or verifies an IP address.
    """
    # Strip potential http/https prefix if passed
    cleaned_target = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    try:
        ip = socket.gethostbyname(cleaned_target)
        return ip
    except socket.gaierror:
        return None

def save_results_json(filepath: str, data: dict):
    """
    Saves dictionary results to a JSON file.
    """
    dirname = os.path.dirname(filepath)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
