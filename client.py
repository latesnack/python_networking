import random
import string
import CRC
import pickle
from socket import *


class Packet:
   'Class that defines a packet'
   #empCount = 0

   def __init__(self, sequence_number, payload):
      self.sequence_number = sequence_number
      self.payload = payload
      self.checksum = CRC.crc(str(payload))
      self.packet_string = str(self.sequence_number) + str(self.payload) + str(self.checksum)
   def displayPacket(self):
     print (self.packet_string)
     print("\n")
    




#Generate a file of 1024 random characters
	
gen_file = open("string.txt", "w")
string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(1024)])
gen_file.write(string)
gen_file.close()

sequence_no = 0
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
	
with open("string.txt", "rb") as f:  #While file is open
    while True:
        payload = f.read(8)          #Read in 8 bytes from file
        if not payload:            
            break  
        newPacket = Packet(sequence_no, payload) 

        #pickle the packet into a byte array
        pickled_packet = pickle.dumps(newPacket)
		#send the packet
        clientSocket.send(pickled_packet)
        acknowledged = 0
        while acknowledged != 1:
            ack_string = clientSocket.recv(1024)
            if ack_string == b"666":
                acknowledged = 1
                print("ack received \n")
        Packet.displayPacket(newPacket)
        sequence_no+=1
		
#Send a special packet that symbolises the end of the file		
end_frame_packet = Packet(-1, 0)
end_pickled = pickle.dumps(end_frame_packet)
clientSocket.send(end_pickled)
#Close the socket
clientSocket.close()
