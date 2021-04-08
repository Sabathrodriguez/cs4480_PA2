#@author: sabath rodriguez
#@classname: controller.py
#@summary: software defined networking controller, used to send flow table to our router. Also used to control "control" plane traffic

from socket import *

class Node:
    def __init__(self):
        self.forwarding_table = "match: sra<=20 and dsa<=20 and srcp>10 and dsp>10 | action: src=21 srp=40 forward(B) | statistics: 0\n" + "match: sra>40 and dsa>40 and srp>10 and dsp>10 | action: src=21 srp=40 forward(B) | statistics: 0\n" + "match: srp<=10 or dsp<=10 | action: drop | statistics: 0\n" + "match: sra>=98 and dsa>98 and srcp<=49 | action: forward(B) | statistics: 0"
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.server_port = 4450
        self.IP = "127.0.0.1"

    #summary: this method takes 0 arguments and starts out server, will listen and wait for 1 connection. When server is connected, it will send the forwarding table to client
    def start_server(self):
        self.socket.bind((self.IP, self.server_port))
        self.socket.listen(1)

        print("server/controller is on")

        #holds on to incoming socket address
        connection_socket, addr = self.socket.accept()
        
        #we will send our forwarding table as a string
        table_as_string = ""

        for str in self.forwarding_table.split("\n"):
            for el in str:
                table_as_string += el + " "

        #sends forwarding table to socket address from client socket connection
        connection_socket.send(self.forwarding_table.encode())
        
        #closes client socket connection, not our socket
        connection_socket.close();

		#closes the controller socket
        self.socket.close()

        
        
        
node = Node()
node.start_server();
