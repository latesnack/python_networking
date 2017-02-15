import random
import string

gen_file = open("string.txt", "w")
string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(1024)])
gen_file.write(string)
gen_file.close()

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
