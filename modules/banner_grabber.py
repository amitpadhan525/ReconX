import socket
SERVICE_MAP = {
    21:  "FTP",
    22:  "SSH",
    23:  "Telnet",
    25:  "SMTP",
    53:  "DNS",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306:"MySQL",
    3389:"RDP",
    8080:"HTTP-Alt",
}

def grab_banner(target,port):
    try:
        s=socket.socket()
        s.settimeout(2)
        s.connect((target,port))
        
        # HTTP detection
        if port in (80,8080):
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())

        banner=s.recv(1024).decode(errors="ignore").strip()
        s.close()

        if banner:
            return banner.split("\n")[0]
        else:
            return SERVICE_MAP.get(port,"No banner")
        

    except (socket.timeout,ConnectionRefusedError,OSError):
        return SERVICE_MAP.get(port,"UNKNOWN")