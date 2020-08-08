import socket
import threading
from encodedecode import encode
from encodedecode import decode 
###############################################################################
#receives data from server and prints on screen
def receive(key):
    full_msg = ''
    new_msg = True
    msglen = 0
    while True:
        msg = ClientSocket.recv(128)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False        
        full_msg += msg.decode("utf-8")
        if len(full_msg)-HEADERSIZE == msglen:
            decodedmessage = decode(key, full_msg[HEADERSIZE:])
            print("\n", decodedmessage)
            new_msg = True
            full_msg = ''
###############################################################################
#input for host ip, port and user's username
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
username = input("Username: ")
key = input("Enter obscurity key: ")
#setup connection to host 
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting to connect")
ClientSocket.connect((host, port))
print("Connected")
###############################################################################
#receive thread to get messages without being blocked
threading._start_new_thread(receive, (key, ))
#this loop gets user input and sends it to the server with the username appended
HEADERSIZE = 10
while True:
    Input = input()
    msg = "{0} said: {1}".format(username,Input)
    msg = encode(key, msg)
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    ClientSocket.send(str.encode(msg))
ClientSocket.close()