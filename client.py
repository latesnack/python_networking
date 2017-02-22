import random
import string
import CRC
import pickle
import struct
from socket import *




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
    

#Generate a file of 1024 random characters
    
gen_file = open("string.txt", "w")
string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(1024)])
gen_file.write(string)
gen_file.close()


#Make an array to store packet
stored_packets = []

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
        #save the packet in case in needs to be resent
        stored_packets.append(newPacket)
        #send the packet
        clientSocket.send(newPacket.packet_struct)
        acknowledged = 0
        while acknowledged != 1:
            #Receive reply from server
            ack_string = clientSocket.recv(1024)
            #If the reply is the preset acknowledgement string, the packet has been acknowledged
            if ack_string == b"666":
                acknowledged = 1
            #Otherwise, the reply is the sequence number of a packet to be resent
            else:
                print("The acknowledgement string is: ")
                print(ack_string)
                blah = ack_string.decode("utf-8")
                print("SENDING BACK: ")
                print(stored_packets[int(blah)].sequence_number)
                clientSocket.send(stored_packets[int(blah)].packet_struct)
        print("acknowledge received \n")
        Packet.displayPacket(newPacket)
        sequence_no+=1
        
#Send a special packet that symbolises the end of the file        
end_frame_packet = Packet(-1, b"11111111111111")
clientSocket.send(end_frame_packet.packet_struct)
#Close the socket
clientSocket.close()
