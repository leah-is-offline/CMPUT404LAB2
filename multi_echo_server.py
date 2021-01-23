import socket
import time
from multiprocessing import Process

HOST = "" #"any host"
PORT = 8001
BUFFER_SIZE = 1024

def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen(2)
        '''In other words, when you call sock.listen(5) and 6 connection
        requests come in before you call accept, one of them is getting dropped
        https://stackoverflow.com/a/48245691'''
        
        while True:
            conn, addr = s.accept()
            p = Process(target = handle_echo, args = (addr,conn))
            p.daemon = True
            p.start()
            print("Started process", p)

def handle_echo(addr, conn):
    print("connected by", addr) 

    full_data = b""
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        full_data+= data
        

    time.sleep(5)
    conn.sendall(full_data) #send data
    conn.shutdown(socket.SHUT_RDWR) #shut down socket
    conn.close()

                
if __name__ == "__main__":
    main()
