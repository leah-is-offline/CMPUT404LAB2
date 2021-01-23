import socket
import sys

L_HOST = ""
L_PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print("getting IP for {h}".format(h = host))
    try:
        remote_ip = socket.gethostbyname( host )
    except Exception as error:
        print(e)
        sys.exit()

    print("IP address of {h} is {rip}".format(h = host, rip = remote_ip))
    return remote_ip


def main():
    o_host = 'www.google.com'
    o_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Starting proxy server")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("host {h} listening on port {p}".format(h = L_HOST, p = L_PORT))
        s.bind((L_HOST,L_PORT))
        s.listen(1)
        
        while True:
            ''' conn is a new socket object usable to send and receive data on the connection,
            and address is the address bound to the socket on the other end of the connection. '''
            
            conn, addr = s.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_endpoint:
                remote_ip = get_remote_ip(o_host) #googles IP
                print("connecting to google: {rip} on port {p}".format(rip = remote_ip, p = o_port))
                s_endpoint.connect((remote_ip, o_port))

                #Forward whatever is received on the server socket to www.google.com
                out_data = conn.recv(BUFFER_SIZE)
                print("sending proxy client data: {od} to google".format(od = out_data))
                s_endpoint.sendall(out_data)
                print("closing socket")
                s_endpoint.shutdown(socket.SHUT_WR)
                '''Shut down one or both halves of the connection. If how is SHUT_RD, further receives are disallowed.
                If how is SHUT_WR, further sends are disallowed'''
                
                #Take the response from www.google.com and send it to the original connection
                in_data = s_endpoint.recv(BUFFER_SIZE)
                print("Sending data from google: {ind} to proxy client".format(ind = in_data))
                conn.send(in_data)#not sendall
                
        conn.close()
            
                
if __name__ == "__main__":
    main()

    
