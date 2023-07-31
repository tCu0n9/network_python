import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = "127.0.0.1"
port = 444
# client kết nối tới server với host và port
client.connect((host,port))

#client gửi một dữ liệu đã được mã hóa tới server
client.send("GET / HTTP/2\r\nHost: google.com\r\n\r\n".encode())

#client nhận được reponse trả về từ server
rep = client.recv(4096)

print(rep.decode())

client.close()