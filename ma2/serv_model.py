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
        self.handle_broadcast(msg=msg, sender='[+] ADMIN ')

        Thread(target=self.client_handler, args=(client,)).start()

    def client_handler(self, c=None):

        client = self.client_group[c]
        while True:
            try:
                msg = client.socket.recv(self.BUFSIZ).decode('utf8')
            except ConnectionResetError:
                print("Connection Dropped on %s %s " % client.address)
                if not msg:
                    self.handle_broadcast(msg='', sender='[+] ADMIN')
                else:
                    self.handle_broadcast(msg=msg, sender='[+] ADMIN')
                del self.client_group[c]
                break
            
            except UnicodeDecodeError:
                print(f'invalid message ')
                pass

            for k, v in self.keywords.items():
                if msg.find(k) != -1:
                    try:
                        keyword_method = getattr(self, str(v))
                    except AssertionError:
                        client.socket.send(bytes("Not following protocol", "utf8"))
                    keyword_method(msg=msg, client=client)

    def handle_broadcast(self, **kwargs):
        recievers = []

        if kwargs.__contains__('msg'):
            msg = kwargs.get('msg')
            if '@broadcast' in msg:
                msg = msg.strip('@broadcast')

        if kwargs.__contains__('client'):
            client = kwargs.get('client')
            msg, recievers = self.handle_private(msg=msg, client=client)
        else:
            msg, recievers = self.handle_private(msg=msg, sender=kwargs.get('sender'))

        try:
            [client.socket.send(bytes(msg, 'utf8')) for rec in recievers for client in self.client_group if client.username == rec]
        except ConnectionResetError:
            pass


    def handle_private(self, **kwargs):
        if kwargs.__contains__('msg'):   
            msg = kwargs.get('msg')
        assert msg != None

        if kwargs.__contains__('client'):
            client = kwargs.get('client')
            sender = client.username
        
        else:
            if kwargs.__contains__('sender'):
                sender = kwargs.get('sender')

        recievers = []

        if msg.find('{') != -1 & msg.find('}') != -1:
            submsg = msg[msg.find('{') + 1: msg.find('}')].split(',')

            for t in submsg:
                recievers.append(t.strip(',').strip(' '))

            submsg1 = msg[:msg.find('{')]
            submsg = msg[msg.find('}') + 1:]
            submsg = f"{sender} : (PRIVATE) {submsg1}{submsg}"

            return submsg, recievers

        else:
            [recievers.append(c.username) for c in self.client_group if c.username != '']
            msg = f"{sender} : {msg}"
            return msg, recievers

    def handle_quit(self, **kwargs):
        print("HANDLE QUIT CALLED")
        client = kwargs.get('client')
        client.socket.send(bytes('Goodbyte', 'utf8'))
        del self.client_group[client]

    def handle_file(self, **kwargs):
        print("handle_file kaldt")
        """ da keywordede private er seperat fra @file og derfor ligger det ansvar under handle_private. 
        Indtil videre har vi håndteret det hér, ved at lede efter @file.
        """
        client = kwargs.get('client')
        header = kwargs.get('msg')
        client = self.client_group[client]
        recievers = []

        header, recievers = self.handle_private(msg=header, client=client) 
        
        file_size = int(header.split("_", 1)[-1].split("_", 1)[0])
        self.BUFSIZ = file_size
        file_encoding = str(header.split("_", 2)[-1])
        print("Size: " + str(file_size) + " bytes" + "  Fileencoding: " + file_encoding)
        print(f'sending header: {header}')

        try:
            [c.socket.send(bytes(header, 'utf8')) for rec in recievers for c in self.client_group if c.username == rec]
        except ConnectionResetError:
            pass

        file_object = client.socket.recv(self.BUFSIZ)
        print(f'sending file object of length {len(file_object)}')

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
