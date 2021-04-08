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
                        print("count: " + str(self.count))
                        byteAddressPair = self.socket.recvfrom(1024)

                        message = byteAddressPair[0]
                        address = byteAddressPair[1]

                        print("message from a: " + str(message))

node_b = B()
node_b.receive_data()
