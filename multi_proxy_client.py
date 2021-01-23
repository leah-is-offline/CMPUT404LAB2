import socket
from multiprocessing import Pool

HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 1024
payload = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

def main():
    
    address = [(HOST,PORT)]
    with Pool() as p:
        p.map(connect, address * 10)

def connect(addr):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(addr)
            s.sendall(payload.encode())
            s.shutdown(socket.SHUT_WR)

            full_data = b""
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                full_data += data
            print(full_data)
            
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
