import socket
 
def setUp():
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('localhost', 33000)
        BUFSIZ = 1024
        sock.connect(ADDR)

        with open('C:/users/Tarkuen/Desktop/QR.png', 'rb') as f:
            bf = f.read()
            sock.sendall(bf,0)

        
        
if __name__ == "__main__":
    setUp()