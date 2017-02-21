import pickle
import random
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
last_sequence = -1
while isEnded == 0:
     
    #listen for incoming data
    packet = connectionSocket.recv(1024)
    #load bytes object back into Packet object using pickle
    recv_packet = pickle.loads(packet)
    #Apply gremlin function to possibly mess up sequence number
    recv_packet.sequence_number = gremlin(recv_packet.sequence_number)  
    #Print the string of the entire packet
    Packet.displayPacket(recv_packet)
    #check the checksum
    checksum = CRC.crc(str(recv_packet.payload))
    #check if the packet is in sequence, and if the checksum is valid
    if (recv_packet.sequence_number != (last_sequence + 1)) or (checksum != recv_packet.checksum):
        #send back the index of the missing packet if not
        connectionSocket.send(str(last_sequence + 1).encode())
        
    #if the sequence is correct...
    else:
        #send an acknowledgement
        connectionSocket.send(b"666")
        print("Acknowledgement sent \n")
        if recv_packet.sequence_number == -1:
            isEnded = 1
        
        
connectionSocket.close()    
    
    
    
    
    
    