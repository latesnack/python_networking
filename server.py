#Iarla Scaife, 14314716, 2017
#JS Engineering: Computer Networks
#Datalink Protocol

import random
import struct
import CRC
from socket import *

#This function takes in an input, and returns the input unchanged 90% of the time, 
#but alters it 10% of the time

def gremlin(input):
    chance = random.randint(1, 10)
    if chance == 5:
        return input + 4
    else:
        return input
    
#This class defines a packet. 
#Each packet has a sequence number, payload and checksum.
#It features a "packet_struct" item which is a C struct that is used to transmit the packet.
    
class Packet:
   'Class that defines a packet'

   def __init__(self, sequence_number, payload):
      self.sequence_number = sequence_number
      self.payload = payload
      self.checksum = CRC.crc(str(payload))
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
#Create an output file to replicate the string into
outfile = open("output.txt", "a")  
isEnded = 0
last_sequence = -1
while isEnded == 0:
     
    #listen for incoming data
    packet = connectionSocket.recv(1024)
    #Unpack the received C struct
    recv_string = struct.unpack("!i8si", packet) 
    print("STRUCT RECEIVED: ")
    print(recv_string)

    #Apply gremlin function to possibly mess up sequence number
    recv_seq = gremlin(recv_string[0])
    
    #check the checksum
    checksum = CRC.crc(str(recv_string[1]))
    
    #check if the packet is in sequence, and if the checksum is valid
    if (recv_seq != (last_sequence + 1)) or (checksum != recv_string[2]):

        #If not, send back the index of the missing packet 
        connectionSocket.send(str(last_sequence + 1).encode())
        
        print("Requested resend of: ")
        print(str(last_sequence + 1).encode())
        
    #if the sequence is correct...
    else:
        #send the pre decided acknowledgement bytes
        connectionSocket.send(b"66666666")
        print("Acknowledgement sent \n")
        #Append the approved packet's payload to the output file.
        outfile.write(recv_string[1].decode("utf-8"))
        last_sequence += 1
    #If the sequence number is -1, the final packet has been sent.
    if recv_string[0] == -1:
        isEnded = 1

        
connectionSocket.close()    
    
    
    
    
    
    
