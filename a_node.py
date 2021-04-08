#@author: sabath rodriguez
#@classname: a_node.py
#@summary: node that sends data to node b. first connects to router node to find node b address

from socket import *
import random

class A:

	def __init__(self):
		self.router_port = 4460
		self.router_IP = "127.0.0.1"
		self.nodeA_socket = socket(AF_INET, SOCK_DGRAM)
		self.data = "this is my data"
		self.srca = ""
		self.desta = ""
		self.srcp = ""
		self.destp = ""

	def send_data(self, message):
                # source address (0-99), dest. address (0-99), source port (0-49), dest. port (0-49)
		self.srca = self.generate_random_data(99)
		self.desta = self.generate_random_data(99)
		self.srcp = self.generate_random_data(49)
		self.destp = self.generate_random_data(49)
		string_a = str(self.srca) +" "+ str(self.desta) +" "+ str(self.srcp) +" "+ str(self.destp) + " \n " + message
		self.nodeA_socket.sendto(string_a.encode(), (self.router_IP, self.router_port))

	def generate_random_data(self, var_max):
		var = str(random.randrange(0,var_max))
		return var
			
		
nodeA = A()
for i in range(0, 100):
        nodeA.send_data('''This is pointless, we shouldnt have to write 508 bytes specifically. This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we shouldnt have to write 508 bytes specifically.
This is pointless, we ye ye ye y
''')
