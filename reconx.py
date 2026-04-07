import argparse
from modules.port_scanner import run_port_scan

def main():
    parser=argparse.ArgumentParser(description="ReconX -Advannced Recon Tool")
    parser.add_argument("-t","--target",required=True,help="Target IP or domian")
    parser.add_argument("-p","--ports",help="Port range (Ex. 1-1000)")
    parser.add_argument("-d","--dir",help="Wordlist for directory scan")

    args=parser.parse_args()

    print(f"Target: {args.target}")

    if args.ports:
        print("\n[PORT SCAN]")
        open_ports=run_port_scan(args.target,args.ports)

        for port in open_ports:
            print(f"{port} -> OPEN")
        print(f"Total OPEN ports {len(open_ports)}")


if __name__== "__main__":
    main()
