import socket
 
def setUp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('localhost', 33000)
        BUFSIZ = 1024
    
        sock.bind(ADDR)
        sock.listen(5)
        c_id, c_a = sock.accept()

        msg = c_id.recv(BUFSIZ*5)
        with open('test.PNG', 'wb') as t:
            t.write(msg)
        
        


if __name__ == "__main__":
    while(1):

        setUp()