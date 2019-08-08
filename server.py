import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import sys
import os
import ssl

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# server_addr = ('0.0.0.0', 8080)
# sock.bind(server_addr)
# sock.listen(1)

listen_addr = '172.18.81.40'
listen_port = 8080
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'
PYTHONHTTPSVERIFY = 0

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.options &= ssl.PROTOCOL_TLS_SERVER
context.options &= ssl.OP_NO_SSLv2
context.options &= ssl.OP_NO_SSLv3
#context.verify_mode = ssl.CERT_REQUIRED

context.load_cert_chain(certfile=server_cert, keyfile=server_key)

context.load_verify_locations(cafile=client_certs)


bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(5)



goodCredentialsOrNot = 0

dirName = '/home/alex/PycharmProjects/chatDir'
fileName = 'chatConversation.txt'
credentialsFileName = 'credentials.txt'
pathToFile = dirName + '/' + fileName
pathToCredentialsFile = dirName + '/' + credentialsFileName

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory ", dirName, "created")

cfile1 = open(pathToCredentialsFile, "a+")
cfile2 = open(pathToCredentialsFile, "r+")

file3 = open(pathToFile, "a+")
file2 = open(pathToFile, "r+")


while True:
    newsocket, fromaddr = bindsocket.accept()
    try:
        conn = context.wrap_socket(newsocket, server_side=True, do_handshake_on_connect=False)
        conn.do_handshake()
        while True:
            clientIp = conn.getpeername()[0]
            print('Connected: ', conn)
            print('IP: ', clientIp)
            data = conn.recv(1024)
            # print(data.decode('utf-8'))
            if data:

                myData = data.decode('utf-8')
                print(myData.split(", "))
                userNameRCV, passRCV, messageRCV = myData.split(", ")
                cfile2 = open(pathToCredentialsFile, "r+")
                readFromCFile = cfile2.readlines()
                for z in readFromCFile:
                    usernameDB, passwordDB = z.split(", ")
                    if (userNameRCV == usernameDB) and (passRCV == passwordDB.rstrip()):
                        userConnected = usernameDB
                        break
                    else:
                        userConnected = 'NoAccount'
                cfile2.close()


                if myData.split(", ")[2] == "#$" and userConnected != 'NoAccount':
                    # case client just want to connect

                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                    conn.send((userConnected + '\n').encode())
                elif userConnected != 'NoAccount' and myData.split(", ")[2] != "#$":
                    #case client sent message
                    file3 = open(pathToFile, "a+")
                    messageToWriteInFile = "Client-" + userConnected + ": " + myData.split(", ")[2]
                    file3.write(messageToWriteInFile + "\n")
                    file3.close()
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                elif userConnected == 'NoAccount':

                    conn.send((userConnected + "\n").encode())
            elif not data:
                break
    finally:
        print("Closing connection")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()


