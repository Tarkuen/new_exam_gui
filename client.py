import unittest
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from ma2.model import TCPClient
from ma2.controller import TCPController

class testTCPClient(unittest.TestCase):

    def setUp(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.ADDR = ('localhost', 33000)
        self.BUFSIZ = 1024

    def test(self):
        self.sock1 = socket(AF_INET, SOCK_STREAM)
        self.sock1.connect(self.ADDR)


if __name__ == "__main__":
    # TCPController()
    result = unittest.main(exit=False)
    if result.result.wasSuccessful():
        TCPController()
    else:
        print('SERVER NOT RUNNING')
        print(result.result)
