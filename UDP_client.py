import socket

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

host = "google.com"
port = 80

client.sendto("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode(),(host,port))

data = client.recvfrom(4096)

print(data)
