#!/usr/bin/env python3
"""
ReconX - Advanced Modular Network Reconnaissance & Enumeration Tool
"""

import argparse
import sys
from datetime import datetime
from modules.port_scanner import run_port_scan
from modules.banner_grabber import grab_banner
from modules.dir_scanner import run_dir_scan
from utils.helpers import parse_ports, resolve_target, save_results_json
from utils.logger import banner_header, info, success, warn, error, Colors

def parse_args():
    parser = argparse.ArgumentParser(
        description="ReconX - Modular Network Reconnaissance & Asset Discovery Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--target", required=True, help="Target hostname or IP address (e.g., example.com, 192.168.1.1)")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., '80', '80,443', '1-1000', '21,22,80-100')")
    parser.add_argument("-d", "--dir", nargs="?", const="wordlists/common.txt", help="Wordlist for web directory enumeration (default: wordlists/common.txt)")
    parser.add_argument("--ssl", action="store_true", help="Force HTTPS for web directory scan")
    parser.add_argument("-o", "--output", default="output/results.json", help="Path to save JSON results (default: output/results.json)")
    parser.add_argument("-w", "--workers", type=int, default=150, help="Number of concurrent threads (default: 150)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    return parser.parse_args()

def main():
    banner_header()
    args = parse_args()

    # Target resolution
    target_ip = resolve_target(args.target)
    if not target_ip:
        error(f"Could not resolve target: {args.target}")
        sys.exit(1)

    info(f"Target: {Colors.BOLD}{args.target}{Colors.RESET} ({target_ip})")
    info(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "target": args.target,
        "target_ip": target_ip,
        "timestamp": datetime.now().isoformat(),
        "open_ports": [],
        "discovered_endpoints": []
    }

    try:
        # 1. Port Scanning & Banner Grabbing
        if args.ports:
            print(f"\n{Colors.CYAN}[*] Starting Port Scan on: {args.ports}{Colors.RESET}")
            open_ports = run_port_scan(
                target_ip,
                args.ports,
                max_workers=args.workers,
                timeout=args.timeout
            )

            if open_ports:
                print(f"\n{'PORT':<8} {'STATUS':<8} {'SERVICE / BANNER'}")
                print("-" * 55)
                for port in open_ports:
                    banner = grab_banner(args.target, port, timeout=args.timeout + 1.0)
                    print(f"{port:<8} {Colors.GREEN}OPEN{Colors.RESET}     {banner}")
                    results["open_ports"].append({
                        "port": port,
                        "status": "OPEN",
                        "banner": banner
                    })
                print("-" * 55)
                success(f"Total open ports found: {len(open_ports)}")
            else:
                warn("No open ports found in specified range.")

        # 2. Directory Scanning
        if args.dir:
            print(f"\n{Colors.CYAN}[*] Starting Web Directory Scan with wordlist: {args.dir}{Colors.RESET}")
            endpoints = run_dir_scan(
                args.target,
                wordlist_path=args.dir,
                use_https=args.ssl,
                max_workers=min(args.workers, 30),
                timeout=args.timeout + 2.0
            )

            if endpoints:
                print(f"\n{'STATUS':<10} {'PATH':<25} {'URL'}")
                print("-" * 65)
                for ep in endpoints:
                    status_col = Colors.GREEN if ep['status'] < 400 else Colors.YELLOW
                    print(f"{status_col}{ep['status']} {ep['reason']:<5}{Colors.RESET} {ep['path']:<25} {ep['url']}")
                    results["discovered_endpoints"].append(ep)
                print("-" * 65)
                success(f"Total discovered paths: {len(endpoints)}")
            else:
                info("No accessible endpoints found with the provided wordlist.")

        # 3. Export Results
        if args.output:
            save_results_json(args.output, results)
            info(f"Results successfully saved to: {Colors.BOLD}{args.output}{Colors.RESET}")

        print(f"\n{Colors.GREEN}[✔] Reconnaissance completed.{Colors.RESET}\n")

    except KeyboardInterrupt:
        warn("\nScan interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
