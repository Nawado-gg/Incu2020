import socket

def main():
    host = '127.0.0.1'
    port = 5000
    
    mySocket = socket.socket()
    mySocket.connect((host, port))
    message = input(">")
    
    print('"q" for quit')
    while message != 'q':
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()
        print('Server: ' + data)
        message = input('>')
        
    mySocket.close()
    
if __name__ == '__main__':
    main()
        
