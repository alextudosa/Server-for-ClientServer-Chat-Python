import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('0.0.0.0', 8080)
sock.bind(server_addr)
sock.listen(1)

dirName = '/home/alex/PycharmProjects/chatDir'
fileName = 'chatConversation.txt'
pathToFile = dirName + '/' + fileName

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory ", dirName, "created")

file3 = open(pathToFile, "a+")
file2 = open(pathToFile, "r+")


while True:
    connection, server_addr = sock.accept()
    try:
        while True:

            print('Connected: ', connection)
            data = connection.recv(1024)
            print(data.decode('utf-8'))
            if data:
                if data.decode('utf-8') == "#$":
                    # case client just want to connect
                    print('Mmodal', "Momsa")
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        connection.send(y.encode())
                    file2.close()
                    connection.send("#$\n".encode())
                else:
                    #case client sent message
                    print('mesaj', 'nu Connect')
                    file3 = open(pathToFile, "a+")
                    file3.write("Client: " + data.decode('utf-8') + "\n")
                    file3.write("Server: " + data.decode('utf-8') + "\n")
                    file3.close()
                file2 = open(pathToFile, "r+")
                f2 = file2.readlines()
                for y in f2:
                    print(y)
                    connection.send(y.encode())
                file2.close()

            elif not data:
                break

    finally:
        connection.close()


