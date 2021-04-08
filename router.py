#@author: sabath rodriguez
#@classname: router.py
#@summary: software defined networking router, used to control data plane traffic

from socket import *
import operator
import re

class Router:
    def __init__(self):
        self.controller_socket = socket(AF_INET, SOCK_STREAM)
        self.router_socket = socket(AF_INET, SOCK_DGRAM)
        self.IP = "127.0.0.1"
        self.server_port = 4450
        self.router_port = 4460
        self.flow_table = []
        self.src_IP = ""
        self.dest_IP = ""
        self.srcp = ""
        self.destp = ""
        self.matches = []
        self.actions = []
        self.statistics = []
        self.table = [[]]
    
    #method used to retrieve flow table from server/controller
    def receive_flowtable(self):
        self.controller_socket.connect((self.IP, self.server_port))
        print("connected")
        for temp in str(self.controller_socket.recv(1024)).split("\n"):
            self.flow_table.append(temp)
        for temp in self.flow_table:
            self.parse_flowtable(temp)

        self.controller_socket.close()

    def start_router(self):
        self.receive_flowtable()
        
        self.router_socket.bind((self.IP, self.router_port))

        while True:

            while True:
                bytesAddressPair = self.router_socket.recvfrom(1024)

                message = bytesAddressPair[0]
                address = bytesAddressPair[1]

                message_bits = self.parse_data(message)
                parsed_transport_data = message_bits[0].split(" ")

                self.src_IP = parsed_transport_data[0]
                self.dest_IP = parsed_transport_data[1]
                self.srcp = parsed_transport_data[2]
                self.destp = parsed_transport_data[3]
					
                for match in self.matches:
                    for action in self.actions:
                        if self.message_action(match, action, self.src_IP, self.srcp, self.dest_IP, self.destp):
                            self.router_socket.sendto(message, ("127.0.0.1",5000))
                print("flowtable: " + str(self.flow_table))
                print("4 byte header: " + str(self.src_IP) + ", " + str(self.dest_IP) + ", " + str(self.srcp) + ", " + str(self.destp))
			

	#returns an array of parsed data, first element is transport info such as IP and port, second element is message
    def parse_data(self, data):
        transport_and_message = str(data.decode()).split("\n")
        transport_info = transport_and_message[0]
        message = transport_and_message[1]
        return [transport_info, message]

    def parse_flowtable(self, data):
        parsed_flowtable = data.split("|")
        for el in parsed_flowtable:
            el.strip()
            if operator.contains(el, "match"):
                self.matches.append(el[6:])
            elif operator.contains(el, "action"):
                self.actions.append(el[8:])
            elif operator.contains(el, "statistics"):
                self.statistics.append(el[12:])

    def message_action(self, match, action, src_IP, src_port, dest_IP, dest_port):
        and_count = 0;
        or_count = 0;
        is_match = True
        match_split = match.strip().split("and")
        #for loop to count and/or's
        for temp in match_split:
            el = temp.strip()
            if not is_match:
                return False;
            comp_number = int(el[-2:])

            if ">" in el:
                if "sra" in el:
                    if not int(src_IP) > comp_number:
                        is_match = False;
                elif "dsa" in el:
                    if not int(dest_IP) > comp_number:
                        is_match = False;
                elif "srcp" in el:
                    if not int(src_port) > comp_number:
                        is_match = False;
                elif "dsp" in el:
                    if not int(dest_port) > comp_number:
                        is_match = False;
            elif ">=" in el:
                if "sra" in el:
                    if not int(src_IP) >= comp_number:
                        is_match = False;
                elif "dsa" in el:
                    if not int(dest_IP) >= comp_number:
                        is_match = False;
                elif "srcp" in el:
                    if not int(src_port) >= comp_number:
                        is_match = False;
                elif "dsp" in el:
                    if not int(dest_port) >= comp_number:
                        is_match = False;
            elif "<" in el:
                if "sra" in el:
                    if not int(src_IP) < comp_number:
                        is_match = False;
                        break
                elif "dsa" in el:
                    if not int(dest_IP) < comp_number:
                        is_match = False;
                        break
                elif "srcp" in el:
                    if not int(src_port) < comp_number:
                        is_match = False;
                        break
                elif "dsp" in el:
                    if not int(dest_port) < comp_number:
                        is_match = False;
                        break
            elif "<=" in el:
                if "sra" in el:
                    if not int(src_IP) <= comp_number:
                        is_match = False;
                        break
                elif "dsa" in el:
                    if not int(dest_IP) <= comp_number:
                        is_match = False;
                        break
                elif "srcp" in el:
                    if not int(src_port) <= comp_number:
                        is_match = False;
                        break
                elif "dsp" in el:
                    if not int(dest_port) <= comp_number:
                        is_match = False;
                        break
        if is_match:
            #src=21 srp=40 forward(B)
            stuff = action.split(" ")
            for parsed_actions in stuff:
                if not parsed_actions == "forward(B)" and not parsed_actions == "drop":
                    num = parsed_actions[-2:]
                    if "src" in parsed_actions:
                        src_IP = num
                    elif "srp" in parsed_actions:
                        srp = num
                    elif "srcp" in parsed_actions:
                        srcp = num
                    elif "dsp" in parsed_actions:
                        dsp = num
                        if parsed_actions == "drop":
                            return False
                            if parsed_actions == "forward(B)":
                                return True
        return True
router = Router()
router.start_router()
#router.message_action([' sra<=20 and dsa<=20 and srcp>10 and dsp>10 ', ' sra>40 and dsa>40 and srp>10 and dsp>10 ', ' srp<=10 or dsp<=10 '], [' src=21 srp=40 forward(B) ', ' src=21 srp=40 forward(B) ', ' drop '], "21", "13", "41", "52")










