import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target,port):
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(1)

        result=sock.connect_ex((target,port))
        sock.close()

        if result==0:
            return port
    

    except:
        pass



def run_port_scan(target,port_range):
    start,end=map(int,port_range.split("-"))
    open_ports=[]

    with ThreadPoolExecutor(max_workers=300) as executor:
        futures=[]

        for port in range(start,end+1):
            futures.append(executor.submit(scan_port,target,port))

        for future in futures:
            result=future.result()
            if result:
                open_ports.append(result)

    return open_ports


