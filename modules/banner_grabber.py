from socket import socket
import socket
def grab_banner(target,port):
    try:
        s=socket.socket()
        s.settimeout(2)
        s.connect((target,port))
        
        # HTTP detection
        if port in (80,8080):
            s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

        banner=s.recv(1024).decode(errors="ignore").strip()
        s.close()

        if banner:
            return banner.split("\n")[0]
        else:
            return "No banner"
        

    except:
        return "UNKNOWN"