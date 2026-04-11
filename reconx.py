import argparse
from modules.port_scanner import run_port_scan
from modules.banner_grabber import grab_banner


def main():
    parser=argparse.ArgumentParser(description="ReconX -Advannced Recon Tool")
    parser.add_argument("-t","--target",required=True,help="Target IP or domian")
    parser.add_argument("-p","--ports",help="Port range (Ex. 1-1000)")
    # parser.add_argument("-d","--dir",help="Wordlist for directory scan")

    args=parser.parse_args()

    print(f"\nTarget: {args.target}")

    if args.ports:
        print("\n[PORT SCAN]")
        open_ports=run_port_scan(args.target,args.ports)

        for port in open_ports:
            banner=grab_banner(args.target,port)
            print(f"{port:<5} -> OPEN | {banner}")
        print(f"Total OPEN ports {len(open_ports)}")
    else:
        print("Please provide port range using -p ")


if __name__== "__main__":
    main()
