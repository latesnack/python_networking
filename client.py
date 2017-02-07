
from socket import *
while 1:

	serverName = 'localhost'
	serverPort = 12000
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))

	sentence = input('Enter lowercase sentence:').encode()
	clientSocket.send(sentence)

	modifiedSentence = clientSocket.recv(1024)
	print ('Received From Server:', modifiedSentence)

clientSocket.close()
