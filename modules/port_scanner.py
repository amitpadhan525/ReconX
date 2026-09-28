"""
Multi-threaded TCP Port Scanner.
"""

import socket
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
from utils.helpers import parse_ports

def scan_port(target: str, port: int, timeout: float = 1.0) -> Union[int, None]:
    """
    Attempts a TCP connection to the specified target and port.
    Returns the port number if open, otherwise None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                return port
    except (socket.timeout, socket.error, OSError):
        return None
    except KeyboardInterrupt:
        raise
    return None

def run_port_scan(target: str, port_input: Union[str, List[int]], max_workers: int = 150, timeout: float = 1.0) -> List[int]:
    """
    Runs multi-threaded scan across target ports.
    """
    if isinstance(port_input, str):
        ports = parse_ports(port_input)
    else:
        ports = port_input

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, target, port, timeout): port for port in ports}

        for future in futures:
            try:
                res = future.result()
                if res is not None:
                    open_ports.append(res)
            except KeyboardInterrupt:
                executor.shutdown(wait=False, cancel_futures=True)
                raise

    open_ports.sort()
    return open_ports
