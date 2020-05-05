import socket, numpy as np

class socketserver:
    def __init__(self, address = '', port = 80):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''
        
    def recvmsg(self):
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print('connected to', self.addr)
        self.cummdata = ''

        while True:
            data = self.conn.recv(10000)
            self.cummdata+=data.decode("utf-8")
            if not data:
                break    
            self.conn.send(bytes(self.cummdata, "utf-8"))
            return self.cummdata

    def sendmsg(self, t_host, t_port, t_msg):
        s.connect(t_host, t_port)
        s.sendall(bytes(t_msg, "utf-8"))

    def __del__(self):
        self.sock.close()