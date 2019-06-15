import socket
 
def setUp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('localhost', 33000)
        BUFSIZ = 1024
        sock.bind(ADDR)
        sock.listen(5)
        c_id, c_a = sock.accept()
        count = 0

        keyword = c_id.recv(BUFSIZ)
        if keyword == b'@file':
            file_size = c_id.recv(BUFSIZ).decode('utf8')
            print(file_size)
            next_file = c_id.recv(int(file_size))
            c_id.send(next_file)
        
if __name__ == "__main__":
   setUp()