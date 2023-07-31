import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "0.0.0.0"
port = 444

server.bind((host,port))

server.listen(5)
print("[*] Server is listening on %s:%d: \n" % (host,port))

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("[*] Request:\n",request.decode())
    
    client_socket.send("ACK".encode())
while True:
    client,addr = server.accept()

    print("[*] Accepting connect from %s:%d" % (addr[0],addr[1]))
    client_handle = threading.Thread(target=handle_client,args=(client,))
    client_handle.start()
    