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




