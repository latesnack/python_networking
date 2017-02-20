import random
import string

class Packet:
   'Class that defines a packet'
   #empCount = 0

   def __init__(sequence_number, payload):
      self.sequence_number = sequence_number
      self.payload = payload
      self.checksum = crc(payload)
      self.packet = str(self.sequence_number) + payload + checksum
   def displayPacket(self):
     print ("Packet:  %d" % self.packet)




#CRC Algorithm, ported from C by Serge Ballesta

POLYNOMIAL = 0x1021
PRESET = 0

def _initial(c):
    crc = 0
    c = c << 8
    for j in range(8):
        if (crc ^ c) & 0x8000:
            crc = (crc << 1) ^ POLYNOMIAL
        else:
            crc = crc << 1
        c = c << 1
    return crc

_tab = [ _initial(i) for i in range(256) ]

def _update_crc(crc, c):
    cc = 0xff & c

    tmp = (crc >> 8) ^ cc
    crc = (crc << 8) ^ _tab[tmp & 0xff]
    crc = crc & 0xffff
    print (crc)

    return crc

def crc(str):
    crc = PRESET
    for c in str:
        crc = _update_crc(crc, ord(c))
    return crc

def crcb(*i):

    crc = PRESET
    for c in i:
        crc = _update_crc(crc, c)
    return crc
	
	
	
	
	
	
	
gen_file = open("string.txt", "w")
string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(1024)])
gen_file.write(string)
gen_file.close()

sequence_no = 0

with open("string.txt", "rb") as f:
    while True:
        payload = f.read(8)
        if not payload:
            break
        newPacket = Packet(payload, sequence_no)
		Packet.displayPacket(newPacket)
        sequence_no++


		

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
