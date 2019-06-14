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
        print("* "*3+" Server bound and listening on %s %s" % self.ADDR +" *"*3)

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
            del(self.client_group[c])

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
                del self.client_group[c]
                self.handle_broadcast(msg=msg)
                break
                
            for k,v in self.keywords.items():
                if msg.find(k)!= -1:
                    getattr(self, str(v))(msg=msg, client = client, sender=client.username)

    def handle_broadcast(self, **kwargs):
        msg = kwargs.get('msg')
        if kwargs.__contains__('sender'):
            sender=kwargs.get('sender')
        
        else:
            sender="[+] ADMIN"
        
        totalmsg = f"{sender} : {msg}"
        for client in self.client_group:  # Sender beskeden til alle klienter
            try:
                client.socket.send(bytes(totalmsg, 'utf8'))
            except ConnectionResetError:
                continue

    def handle_private(self, **kwargs):

        msg = kwargs.get('msg')
        client = kwargs.get('client')

        assert msg.find('{') != -1
        assert msg.find('}') != -1
        recievers = []

        start = msg.find('{')
        end = msg.find('}')

        submsg = msg[start+1 : end].split(',')

        for t in submsg:
            recievers.append(t.strip(',').strip(' '))
        
        submsg = msg[end+1:]
        [c.socket.send(bytes(client.username + ": (PRIVATE) "+submsg, 'utf8')) for rec in recievers for c in self.client_group if c.username == str(rec)]

    def handle_quit(self, **kwargs):
        pass

    def handle_file(self, **kwargs):
        return "HANDLED FILE"


"""  # if msg.startswith('@'):
            #     temp = msg.split(" ", 3)

            #     if (temp[0] == self.keywords[0]):
            #         client.close()
            #         del self.client_group[c]

            #     else:
            #         target = temp[0].strip("@")

            #         if temp[1] is not None and temp[1] == self.keywords[1]:

            #             for c in self.client_group:
            #                 if c.username == target:
            #                     username = f"{c.username}"
            #                     keyword = str(self.keywords[1])
            #                     target= f"{temp[2]}"
            #                     msg = username+' '+keyword+' '+target
            #                     c.socket.send(bytes( msg, "utf8"))

            #                     print('routing data...')
            #                     while True:
            #                         fil = c.socket.recv(self.BUFSIZ)
            #                         if fil[-4:] == bytes("done", 'utf8'):
            #                             c.socket.send(fil[:-4])
            #                             c.socket.send(bytes("done", 'utf8'))
            #                             break
            #                         else:
            #                             c.socket.send(fil)
            #                     print(f"Transferred file to {c.username} by type {temp[2]}")
            #         else:
            #             for c in self.client_group:
            #                 if c.username == target:
            #                     msg = client.username + ': (PRIVATE) ' + msg
            #                     c.socket.send(bytes(msg, "utf8"))

            # else:
            #     self.broadcast(msg, sender=client.username) """

class Client:

    def __init__(self, socket=None, address='', username=''):
        self.address = address
        self.socket = socket
        self.username = username


class Protocol:

    def __init__(self):
        self.keywords= {}
        with open('protocol.json', 'r') as f:
            keys = json.load(f)

        for k,v in keys.items():
            self.keywords.update({k:v})
        
    def getKeywords(self):
        return self.keywords

if __name__ == "__main__":
    a = MyTCPServer()