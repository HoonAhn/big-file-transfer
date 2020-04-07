import socketserver
from os.path import exists

HOST = ''
PORT = 9009
BUFFER = 1024

class BigTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        transferred_data = 0
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

def run_server():
    print("<SERVER>: Big File Server Started")

    try:
        server = socketserver.TCPServer((HOST,PORT), BigTCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("<SERVER>: End Big File Server")

run_server()
