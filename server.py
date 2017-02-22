import pickle
import random
import struct
import CRC
from socket import *

def gremlin(input):
    chance = random.randint(1, 10)
    print("random function returned: ")
    print(str(chance))
    if chance == 5:
        return input + 4
    else:
        return input
    
    
class Packet:
   'Class that defines a packet'
   #empCount = 0

   def __init__(self, sequence_number, payload):
      self.sequence_number = sequence_number
      self.payload = payload
      self.checksum = CRC.crc(str(payload))
      #self.packet_string = str(self.sequence_number) + str(self.payload) + str(self.checksum)
      self.packet_struct = struct.pack("!i8si", self.sequence_number, self.payload, self.checksum)
   def displayPacket(self):
     print (self.packet_struct)
     print("\n")
    

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
    
isEnded = 0
last_sequence = -1
while isEnded == 0:
     
    #listen for incoming data
    packet = connectionSocket.recv(1024)

    recv_string = struct.unpack("!i8si", packet) 
    print("STRUCT RECEIVED: ")
    print(recv_string)
    #Apply gremlin function to possibly mess up sequence number
    recv_seq = recv_string[0]
    
    #check the checksum
    checksum = CRC.crc(str(recv_string[1]))
    
    #check if the packet is in sequence, and if the checksum is valid
    if (recv_seq != (last_sequence + 1)) or (checksum != recv_string[2]):
        #send back the index of the missing packet if not
        connectionSocket.send(str(last_sequence + 1).encode())
        
        print("Requested resend of: ")
        print(str(last_sequence + 1).encode())
        
    #if the sequence is correct...
    else:
        #send an acknowledgement
        connectionSocket.send(b"666")
        print("Acknowledgement sent \n")
        last_sequence += 1
    if recv_string[0] == -1:
        isEnded = 1

        
connectionSocket.close()    
    
    
    
    
    
    