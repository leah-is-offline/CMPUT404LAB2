import socket,sys


HOST = '127.0.0.1'
PORT = 8001
payload = 'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
BUFFER_SIZE = 1046

def main():
    
    s = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST,PORT))
            s.sendall(payload.encode())
            s.shutdown(socket.SHUT_WR)
            received_data = s.recv(BUFFER_SIZE)
            print(received_data)
    except Exception as e:
        print(e)
    finally:
        if s is not None:
            s.close()

        
if __name__ == "__main__":
    main()

    
    
