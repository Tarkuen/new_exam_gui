import unittest
from socket import socket, AF_INET, SOCK_STREAM

from ma2.serv_model import MyTCPServer

class testTcpServer(unittest.TestCase):
    
    def setUp(self):
        self.client_group = {}
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.ADDR = ('localhost', 33000)
        self.BUFSIZ = 1024
        self.sock.bind(self.ADDR)
        self.sock.listen(5)

    def testSocket(self):
        self.sock1 = socket(AF_INET, SOCK_STREAM)
    
        self.sock1.connect(self.ADDR)
        self.hostaddr, self.port = self.sock1.getpeername()
        self.assertEqual(self.hostaddr, '127.0.0.1')
        self.assertEqual(self.port, 33000)
        self.assertNotEqual(self.port,33002)
        

    def tearDown(self):
        self.sock.close


if __name__ == '__main__':
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        MyTCPServer()
    else:
        print("FREE UP IP AND PORT - ALREADY IN USE")
        print(result.warnings)

