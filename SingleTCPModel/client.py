import socket
from os.path import exists
from os import mkdir

HOST = "localhost"
PORT = 9009
BUFFER = 1024

def get_bigfile_from_server(filename):
    transferred_data = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(filename.encode())

        data = sock.recv(BUFFER)
        if not data:
            print("<CLIENT>: File does not exisits or got error during transfer. [%s]" % filename)
            return
        if not exists("download/"):
            print("No Directory")
            mkdir("download/")
        with open("download/"+filename, 'wb') as f:
            try:
                while data:
                    f.write(data)
                    transferred_data += len(data)
                    data = sock.recv(BUFFER)
            except Exception as e:
                print(e)
    print("<CLIENT>: Recieved big file [%s], transferred data [%d]" % (filename, transferred_data))

filename = input("Enter file name to download: ")
get_bigfile_from_server(filename)