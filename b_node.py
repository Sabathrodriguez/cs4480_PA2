#@author: sabath rodriguez
#@classname: b_node.py
#@summary: node that receives data from node a

from socket import *

class B:
    def __init__(self):
        self.IP = "127.0.0.1"
        self.port = 5000
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.data = ""
        self.count = 0

    def receive_data(self):
        self.socket.bind((self.IP, self.port))
        while True:
                print("node b is ready to receive...")
                self.count += 1
                byteAddressPair = self.socket.recvfrom(1024)

                message = byteAddressPair[0]
                address = byteAddressPair[1]
                
                message_bits = self.parse_data(message)
                parsed_transport_data = message_bits[0].split(" ")

                src_IP = parsed_transport_data[0]
                dest_IP = parsed_transport_data[1]
                srcp = parsed_transport_data[2]
                destp = parsed_transport_data[3]

                print("4 byte header: " + str(src_IP) + ", " + str(dest_IP) + ", " + str(srcp) + ", " + str(destp))
                
    def parse_data(self, data):
        transport_and_message = str(data.decode()).split("\n")
        transport_info = transport_and_message[0]
        message = transport_and_message[1]
        return [transport_info, message]

node_b = B()
node_b.receive_data()
