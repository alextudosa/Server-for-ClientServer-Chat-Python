import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('0.0.0.0', 8080)
sock.bind(server_addr)
sock.listen(1)



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
    connection, server_addr = sock.accept()
    try:
        while True:
            clientIp = connection.getpeername()[0]
            print('Connected: ', connection)
            print('IP: ', clientIp)
            data = connection.recv(1024)
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


