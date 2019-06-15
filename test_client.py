import socket
import os
 
def setUp():
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('localhost', 33000)
        BUFSIZ = 1024
        sock.connect(ADDR)
        sock.send(bytes("@file", "utf8"))

        print('sending all')

        path = 'C:/users/Tarkuen/Desktop/QR.png'
        with open(path, 'rb') as f:
            size = os.path.getsize(path)
            print(size)
            BUFSIZ = size

            sock.send(bytes(str(size),'utf8'))
            sock.sendall(f.read(),0)

            f.close()
        
        count = 0
        echo_file = sock.recv(BUFSIZ)
        while count < 2:
            with open('test'+str(count)+'.PNG', 'wb') as t:
                t.write(echo_file)
                t.close
                count+=1

        
if __name__ == "__main__":
    setUp()