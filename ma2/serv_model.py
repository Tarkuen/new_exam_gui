import json

from socket import AF_INET, socket, SOCK_STREAM  # AF_INET & SOCK_STREAM for TCP sockets
from threading import Thread


class MyTCPServer:

    def __init__(self, adress='localhost', port=33000):
        self.p = Protocol()
        self.client_group = {}
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.ADDR = (adress, port)
        self.BUFSIZ = 1024
        self.keywords = {}
        self.keywords = self.p.getKeywords()

        self.connection_handler()

    def connection_handler(self):
        self.sock.bind(self.ADDR)
        print("* " * 3 + " Server bound and listening on %s %s" % self.ADDR + " *" * 3)

        while True:
            self.sock.listen(5)
            c_id, c_a = self.sock.accept()

            client = Client(socket=c_id, address=c_a)

            msg = "%s:%s connected." % c_a
            print(msg)

            self.client_group.update({client: client})

            client.socket.send(bytes(msg, 'utf8'))

            Thread(target=self.client_username_handler, args=(client,)).start()

    def client_username_handler(self, c=None):
        client = self.client_group[c]
        try:

            client.socket.send(bytes(" Please select Username (no spaces)", 'utf8'))

        except ConnectionResetError:
            print('Incorrect Username Attempt')
            del (self.client_group[c])

        try:
            username = client.socket.recv(self.BUFSIZ).decode("utf-8")
        except ConnectionResetError:
            return

        if username.find(' ') != -1:
            raise ConnectionResetError

        msg = "Username connected: %s" % username
        client.socket.send(bytes(msg, 'utf8'))

        client.username = username
        self.handle_broadcast(msg=msg)

        Thread(target=self.client_handler, args=(client,)).start()

    def client_handler(self, c=None):

        client = self.client_group[c]
        while True:
            try:
                msg = client.socket.recv(self.BUFSIZ).decode('utf8')
            except ConnectionResetError:
                print("Connection Dropped on %s %s " % client.address)
                self.handle_broadcast(msg=msg)
                del self.client_group[c]

                break

            for k, v in self.keywords.items():
                if msg.find(k) != -1:
                    try:
                        getattr(self, str(v))(msg=msg, client=client, sender=client.username)
                    except AssertionError:
                        client.socket.send(bytes("Not following protocol", "utf8"))

    def handle_broadcast(self, **kwargs):
        msg = kwargs.get('msg')
        if kwargs.__contains__('sender'):
            sender = kwargs.get('sender')

        else:
            sender = "[+] ADMIN"

        totalmsg = f"{sender} : {msg}"
        for client in self.client_group:  # Sender beskeden til alle klienter
            try:
                client.socket.send(bytes(totalmsg, 'utf8'))
            except ConnectionResetError:
                continue

    def handle_private(self, **kwargs):
        print("handle_private kaldt")

        msg = kwargs.get('msg')
        client = kwargs.get('client')

        assert msg.find('{') != -1
        assert msg.find('}') != -1
        recievers = []
        submsg = msg[msg.find('{') + 1: msg.find('}')].split(',')

        for t in submsg:
            recievers.append(t.strip(',').strip(' '))

        submsg1 = msg[:msg.find('{')]
        submsg = msg[msg.find('}') + 1:]
        submsg = submsg1 + submsg
        [c.socket.send(bytes(client.username + ": (PRIVATE) " + submsg, 'utf8')) for rec in recievers for c in
         self.client_group if c.username == str(rec)]

    def handle_quit(self, **kwargs):
        print("HANDLE QUIT CALLED")
        client = kwargs.get('client')
        client.socket.send(bytes('Goodbyte', 'utf8'))
        del self.client_group[c]

    def handle_file(self, **kwargs):
        print("handle_file kaldt")
        """ da keywordede private er seperat fra @file og derfor ligger det ansvar under handle_private. 
        Indtil videre har vi håndteret det hér, ved at lede efter @file.
        """
        client = kwargs.get('client')
        header = kwargs.get('msg')
        client = self.client_group[client]

        recievers = []
        if header.find('{')!= -1 & header.find('}')!=-1:
            submsg = header[header.find('{') + 1: header.find('}')].split(',')
            for t in submsg:
                recievers.append(t.strip(',').strip(' '))
        else:
            [recievers.append(c.username) for c in self.client_group]
        
        file_size = int(header.split("_", 1)[-1].split("_", 1)[0])
        self.BUFSIZ = file_size
        file_encoding = str(header.split("_", 2)[-1])
        print("Size: " + str(file_size) + " bytes" + "  Fileencoding: " + file_encoding)

        try:
            [c.socket.send(bytes(header, 'utf8')) for rec in recievers for c in self.client_group if c.username == rec]
        except ConnectionResetError:
            pass
        file_object = client.socket.recv(self.BUFSIZ)
        try:
            [c.socket.send(bytes(file_object)) for rec in recievers for c in self.client_group if c.username == rec]
        except ConnectionResetError:
            pass

        self.BUFSIZ = 1024

        return "HANDLED FILE"

class Client:

    def __init__(self, socket=None, address='', username=''):
        self.address = address
        self.socket = socket
        self.username = username


class Protocol:

    def __init__(self):
        self.keywords = {}
        with open('protocol.json', 'r') as f:
            keys = json.load(f)

        for k, v in keys.items():
            self.keywords.update({k: v})

    def getKeywords(self):
        return self.keywords


if __name__ == "__main__":
    a = MyTCPServer()
