import socket
import time
import threading

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
        with open("download/"+filename, 'wb') as f:
            try:
                while data:
                    f.write(data)
                    transferred_data += len(data)
                    data = sock.recv(BUFFER)
            except Exception as e:
                print(e)
    print("<CLIENT>: Recieved big file [%s], transferred data [%d]" % (filename, transferred_data))

if __name__ == "__main__":
    print("TCP Client Starts")

    while True:
        filename = input("Enter file name to download: ")
        if filename.lower() == 'q' or filename.lower() == 'quit':
            print("Client Terminated")
            break
        get_bigfile_from_server(filename)
        