import socketserver
from threading import Thread, Lock
from os.path import exists

HOST = ''
PORT = 9009
BUFFER = 1024

th_lock = Lock()

class BigTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):

        transferred_data = 0
        with th_lock:
            print("<SERVER>: Connected to [%s]" % self.client_address[0])
            filename = self.request.recv(BUFFER)
            filename = filename.decode()
            # If the file doesn't exists, return from the handle function
            if not exists(filename):
                return
            
            print("<SERVER>: Start transferring file [%s]" % filename)
            with open(filename, 'rb') as f:
                try:
                    data = f.read(BUFFER)
                    while data:
                        transferred_data += self.request.send(data)
                        data = f.read(BUFFER)
                except Exception as e:
                    print(e)
            print("<SERVER>: Completed transfer file [%s], transferred data [%d]" % (filename,transferred_data))

class TCPServerThread(Thread):
    socketserver.TCPServer.allow_reuse_address = True
    server = None

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        if not self.server is None:
            self.server.shutdown()
            self.server = None
        try:
            server = socketserver.TCPServer((HOST,PORT), BigTCPHandler)
            with th_lock:
                print("<SERVER>: Big File Server Thread Started")
                print("Listening on port[%d]" % PORT)
            server.serve_forever()
            with th_lock:
                print("<SERVER>: Big File Server Thread Terminated")
        except KeyboardInterrupt:
            print("<SERVER>: Big File Server Thread Terminated on KeyboardInterrupt")
    
    def stop(self):
        self.server.shutdown()
        self.server = None

server_thread = None

def start_server():
    stop_server()

    global server_thread
    server_thread = TCPServerThread()
    server_thread.start()

def stop_server():
    global server_thread
    if not server_thread is None:
        server_thread.stop()
        server_thread.join()
        server_thread = None

