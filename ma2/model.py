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
            incoming_msg = self.sock.recv(self.BUFSIZ).decode('utf8')
            if incoming_msg.find("@file_") != -1:

                file_encoding = incoming_msg.split("_", 2)[-1]
                file_size = incoming_msg.split("_", 1)[-1].split("_", 1)[0]
                print(file_encoding + " " + str(file_size))
                self.BUFSIZ = int(file_size)

                # os.chdir("STI TIL HVOR BILLEDET SKAL GEMMES")
                with open('newfile.' + file_encoding, 'wb') as f:
                    print('Recieving File, saved as %s ' % 'newfile.'+file_encoding)
                    fil = self.sock.recv(self.BUFSIZ)
                        # if fil[-4:] == bytes("done", 'utf8'):
                        #     f.write(fil[:-4])
                        #     break
                        # else:
                            # f.write(fil)
                    f.write(fil)
                    f.close()

                info = incoming_msg.split(" ", 1)
                return f"Recieved File from {info[0]}"

            return incoming_msg

        except OSError:
            return -1

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
                # line = f.read(self.BUFSIZ)
                # while line:
                #     self.sock.sendall(line)
                #     line = f.read(self.BUFSIZ)
        except FileNotFoundError:
                    return f"File Not found and not sent to: {target[0]}"
                
        self.sock.send(bytes("done", 'utf8'))
        return f"Sucessfully sent file to {target[0]}"
