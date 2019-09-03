import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import sys
import os
import ssl
import os.path
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
# fileName = 'chatConversation.txt'
credentialsFileName = 'credentials.txt'
isTyping = "isTyping.txt"
# pathToFile = dirName + '/' + fileName
pathToCredentialsFile = dirName + '/' + credentialsFileName
pathToIsTyping = dirName + '/' + isTyping

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory ", dirName, "created")

cfile1 = open(pathToCredentialsFile, "a+")
cfile2 = open(pathToCredentialsFile, "r+")



tfile1 = open(pathToIsTyping, "a+")
tfile2 = open(pathToIsTyping, "r+")


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
            isTyping = 0
            # print(data.decode('utf-8'))
            if data:

                myData = data.decode('utf-8')
                print(myData.split(", "))
                userNameRCV, passRCV, protocol, talkTo, messageRCV = myData.split(", ")
                cfile2 = open(pathToCredentialsFile, "r+")
                readFromCFile = cfile2.readlines()
                for z in readFromCFile:
                    usernameDB, passwordDB = z.split(", ")
                    if (userNameRCV == usernameDB) and (passRCV == passwordDB.rstrip()):
                        userConnected = usernameDB
                        break
                    else:
                        userConnected = 'NoAccount'
                for y in readFromCFile:
                        usernameDB1, passwordDB1 = y.split(", ")
                        if talkTo in "":
                            talkingTo = "NoUserToTalk"
                        elif talkTo in usernameDB1:
                            talkingTo = usernameDB1
                            break;
                        else:
                            talkingTo = "NoUserToTalk"
                if userConnected == talkingTo:
                    talkingTo = "CannotTalkToYourself"
                cfile2.close()


                if userConnected not in "NoAccount" and talkingTo not in "NoUserToTalk" \
                        and talkingTo not in "CannotTalkToYourself":
                    fileName = userConnected + "_" + talkingTo + ".txt"
                    pathToFile1 = dirName + '/' + fileName
                    fileName1 = talkingTo + "_" + userConnected + ".txt"
                    pathToFile2 = dirName + '/' + fileName1
                    if os.path.exists(pathToFile1):
                        pathToFile = pathToFile1
                    elif os.path.exists(pathToFile2):
                        pathToFile = pathToFile2
                    else:
                        pathToFile = pathToFile1
                    file3 = open(pathToFile, "a+")
                    file2 = open(pathToFile, "r+")
                    file3.close()
                    file2.close()

                if myData.split(", ")[2] == "connect" and userConnected != 'NoAccount' and talkingTo != "NoUserToTalk" and talkingTo not in "CannotTalkToYourself":
                    # case client just want to connect

                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                    tfile2 = open(pathToIsTyping, "r+")
                    tf2 = tfile2.readlines()
                    for v in tf2:
                        if "0" not in v:
                            conn.send(("connect\n").encode())
                        else:
                            conn.send((myData.split(", ")[2] + "\n").encode())
                    tfile2.close()
                elif myData.split(", ")[2] == "refresh" and userConnected != 'NoAccount' and talkingTo != "NoUserToTalk" and talkingTo not in "CannotTalkToYourself":
                    # case refresh conversation
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                    tfile2 = open(pathToIsTyping, "r+")
                    tf2 = tfile2.readlines()
                    for v in tf2:
                        print(v)
                        if '0' not in v:
                            conn.send(v.encode())
                            conn.send((myData.split(", ")[2] + "\n").encode())
                        else:
                            conn.send((myData.split(", ")[2] + "\n").encode())
                    tfile2.close()
                elif userConnected != 'NoAccount' and myData.split(", ")[2] != "connect" \
                        and myData.split(", ")[2] != "typing" and myData.split(", ")[2] != 'not typing' \
                        and myData.split(", ")[2] != "refresh" and myData.split(", ")[2] == "new message" \
                        and talkingTo != "NoUserToTalk" and talkingTo not in "CannotTalkToYourself":
                    #case client sent message
                    file3 = open(pathToFile, "a+")
                    messageToWriteInFile = "Client-" + userConnected + ": " + messageRCV
                    file3.write(messageToWriteInFile + "\n")
                    file3.close()
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                    conn.send((myData.split(", ")[2] + "\n").encode())
                elif userConnected == 'NoAccount':
                    conn.send((userConnected + "\n").encode())
                elif talkingTo == "NoUserToTalk":
                    conn.send(("No user to talk to!\n").encode())
                elif talkingTo == "CannotTalkToYourself":
                    conn.send(("Cannot Talk To Yourself!\n").encode())
                elif myData.split(", ")[2] == "typing" and userConnected != 'NoAccount' and talkingTo != "NoUserToTalk" and talkingTo not in "CannotTalkToYourself":
                    whoIsTyping = myData.split(", ")[2]

                    # print(myData.split(", ")[2])
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    file2.close()
                    conn.send((myData.split(", ")[2] + "\n").encode())
                    tfile1 = open(pathToIsTyping, "w+")
                    tfile1.write(userConnected + " is typing...\n")
                    tfile1.close()
                elif myData.split(", ")[2] == 'not typing' and userConnected != 'NoAccount' and talkingTo != "NoUserToTalk":
                    file2 = open(pathToFile, "r+")
                    f2 = file2.readlines()
                    for y in f2:
                        print(y)
                        conn.send(y.encode())
                    conn.send((myData.split(", ")[2] + "\n").encode())
                    file2.close()
                    tfile1 = open(pathToIsTyping, "w+")
                    tfile1.write("0" + "\n")
                    tfile1.close()
            elif not data:
                break
    finally:
        print("Closing connection")
        # conn.shutdown(socket.SHUT_RDWR)
        conn.close()


