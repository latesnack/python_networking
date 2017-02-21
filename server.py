import pickle
import CRC
from socket import *


class Packet:
   'Class that defines a packet'

   def __init__(self, sequence_number, payload):
      self.sequence_number = sequence_number
      self.payload = payload
      self.checksum = crc(str(payload))
      self.packet_string = str(self.sequence_number) + str(self.payload) + str(self.checksum)
   def displayPacket(self):
     print (self.packet_string)
     print("\n")
    


	
	
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
	
isEnded = 0

while isEnded == 0:
     
	#listen for incoming data
    packet = connectionSocket.recv(1024)
	#load bytes object back into Packet object using pickle
    recv_packet = pickle.loads(packet)
	#Print the string of the entire packet
    Packet.displayPacket(recv_packet)
	
	#check the checksum
    checksum = CRC.crc(str(recv_packet.checksum))
    if checksum == recv_packet.payload:
        #send an acknowledgement
        connectionSocket.send(b"666")
        print("Acknowledgement sent \n")
    if recv_packet.sequence_number == -1:
	    isEnded = 1
connectionSocket.close()	
	
	
	
	
	
	