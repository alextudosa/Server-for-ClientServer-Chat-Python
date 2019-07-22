import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('0.0.0.0', 8080)
sock.bind(server_addr)
sock.listen(1)


user1 = 'alex'
password1 = 'pass1'
user2 = 'vali'
password2 = 'pass2'
goodCredentialsOrNot = 0

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
            clientIp = connection.getpeername()[0]

            print('Connected: ', connection)
            data = connection.recv(1024)
            print(data.decode('utf-8'))
            if data:

                myData = data.decode()
                c = myData.split(", ")
                if c.__contains__(user1) and c.__contains__(password1):
                    userConnected = user1
                elif c.__contains__(user2) and c.__contains__(password2):
                    userConnected = user2
                else:
                    userConnected = 'NoAccount'


                if myData.split(", ")[2] == "#$" and userConnected != 'NoAccount':
                    # case client just want to connect

                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        connection.send(y.encode())
                    file2.close()
                    connection.send((userConnected + '\n').encode())
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
                        connection.send(y.encode())
                    file2.close()
                elif userConnected == 'NoAccount':

                    connection.send((userConnected + "\n").encode())
            elif not data:
                break

    finally:
        connection.close()


