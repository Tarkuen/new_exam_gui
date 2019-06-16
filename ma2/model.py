import json
import os

import requests
from socket import AF_INET, socket, SOCK_STREAM


class TCPClient:

    def __init__(self, adress='localhost', port=33000):
        self.BUFSIZ = 1024
        self.ADDR = (adress, port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.ADDR)
        self.keywords = []
        with open('protocol.json', 'r') as f:
            keys = json.load(f)

        for k,v in keys.items():
            self.keywords.append(v)

    def receive(self):

        try:
            incoming_msg = self.sock.recv(self.BUFSIZ)
            if '@file' in incoming_msg.decode('utf8'):
                print('infile')
                incoming_msg = incoming_msg.decode('utf8')

                file_encoding = incoming_msg.split("_", 2)[-1]
                file_size = incoming_msg.split("_", 1)[-1].split("_", 1)[0]
                print(self.BUFSIZ)
                self.BUFSIZ = int(file_size)

                fil = self.sock.recv(self.BUFSIZ)
                fil = self.sock.recv(self.BUFSIZ)

                # os.chdir("STI TIL HVOR BILLEDET SKAL GEMMES")

                with open(f"newfile.{file_encoding}", 'wb') as f:
                    print(f"Recieving File, saved as newfile.{file_encoding} of size {self.BUFSIZ}")
                    f.write(fil)
                    f.close()

                self.BUFSIZ = 1024
                info = incoming_msg.split(" ", 1)
                return f"Recieved File from {info[0]}"

            return incoming_msg

        except OSError:
            print('OSERROR')
            return -1
        return incoming_msg

    def send(self, my_msg, event=None):
        try:
            self.sock.send(bytes(my_msg, "utf-8"))
        except OSError:
            self.sock.close()
            return -1

    def shutdown(self):
        self.sock.close()

    def sendFile(self, path, my_msg, event=None):
        target = my_msg.split(' ', 1)
        my_msg = my_msg + ' ' + str(path.split('.', 1)[-1])
        try:
            with open(path, 'rb') as f:
                bf = f.read()
                self.sock.sendall(bf, 0)
        except FileNotFoundError:
                    return f"File Not found and not sent to: {target[0]}"
                
        return f"Sucessfully sent file to {target[0]}"
