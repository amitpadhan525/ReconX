"""
Service banner grabber module with SSL and HTTP/HTTPS support.
"""

import socket
import ssl

SERVICE_MAP = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8000: "HTTP-Alt",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

def grab_banner(target: str, port: int, timeout: float = 2.0) -> str:
    """
    Connects to the open port and attempts to extract the service banner.
    """
    is_ssl = port in (443, 8443, 993, 995, 465)
    
    try:
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.settimeout(timeout)

        if is_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(raw_sock, server_hostname=target)
        else:
            s = raw_sock

        s.connect((target, port))

        # Send HTTP probe for web ports
        if port in (80, 8080, 8000, 8888, 443, 8443):
            probe = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: ReconX/1.0\r\nConnection: close\r\n\r\n"
            s.sendall(probe.encode())

        banner_bytes = s.recv(1024)
        s.close()

        banner = banner_bytes.decode("utf-8", errors="ignore").strip()
        if banner:
            # Extract first line or Server header if HTTP
            lines = banner.split("\r\n")
            server_line = next((l for l in lines if l.lower().startswith("server:")), None)
            if server_line:
                return f"{lines[0]} ({server_line})"
            return lines[0][:80]
        else:
            return SERVICE_MAP.get(port, "No banner response")

    except (socket.timeout, ConnectionRefusedError, ssl.SSLError, OSError):
        return SERVICE_MAP.get(port, "Unknown Service")