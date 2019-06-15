import socket
import os
 
def setUp():
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('localhost', 33000)
        BUFSIZ = 1024
        sock.connect(ADDR)
        path = 'C:/Users/Ludvig/Pictures/hund.jpg'
        with open(path , 'rb') as f:
            bf = f.read()
            print(os.path.getsize(path))
            sock.sendall(bf,0)

        
        
if __name__ == "__main__":
    setUp()