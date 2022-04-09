import string   
import random 
import hashlib    
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy 
import sys
import json
import os

S1 = 10 # num of digits of the random keywords
S2 = 16 # num of digits of the tickets
n = 5
ports = [8001,8002,8003,8004,8005]
threshhold = len(ports)/2
# %%
class Node:
    def __init__(self, port, S1, S2, n, name, ports):
        self.port = port
        self.nouce_length = S1
        self.ticket_length = S2
        self.n = n
        self.name = name
        self.routes_info = {}
        self.nouce_map = {}
        self.ticket_map = {}
        self.known = set()
        self.add_others(ports)

    def randomString(self, k):  
        ranKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k = k)) 
        return ranKey

    def get_nouce(self, route:str):
        print("The nouce is generated in this server and boardcast to others")
        if route in self.routes_info.keys():
            nouce = self.randomString(S1)
            self.add_nouce(nouce, route)
            self.boardcast_nouce(nouce, route)
            return nouce, n
        else:
            return False

    def get_ticket(self, key: str):
        print("keyword validation and buy ticket request is processed in this server")
        nouce = key[:S1]
        if nouce not in self.nouce_map.keys():
            return False
        key2 = key.encode('ascii')
        outcome = hashlib.sha256(key2).hexdigest()
        checker = "0" * n
        if outcome[:n] != checker:
            return False
        else:
            ticket = self.randomString(S2)
            route_id = self.nouce_map[nouce]
            if self.boardcast_propose(ticket, route_id):
                if self.boardcast_buy(ticket, route_id):
                    self.add_ticket(ticket, route_id)
                return ticket
            return False
    
    def boardcast_propose(self, ticket:str, route_id:str):
        agree = 1
        for other in self.known.copy():
            try:
                server = ServerProxy(other)
                if(server.propose_check(ticket,route_id)):
                    agree += 1
                else:
                    continue
            except OSError:
                self.known.remove(other)
        if agree > threshhold:
            return True
        else:
            return False

    def boardcast_buy(self, ticket:str, route_id:str):
        agree = 1
        for other in self.known.copy():
            try:
                server = ServerProxy(other)
                if(server.add_ticket(ticket,route_id)):
                    agree += 1
                else:
                    continue
            except OSError:
                self.known.remove(other)
        if agree > threshhold:
            return True
        else:
            return False

    def propose_check(self, ticket:str, route_id:str):
        if self.routes_info[route_id]["Remain"] > 0:
            return True
        else:
            return False

    def add_ticket(self, ticket:str, route_id:str):
        if self.routes_info[route_id]["Remain"] > 0:
            self.routes_info[route_id]["Remain"] -= 1     
            self.ticket_map[ticket] = {"valid": True, "route_id":route_id}
            print(self.ticket_map)
            return True
        else:
            return False

    def boarding_check(self, ticket:str):
        if ticket in ticketList:
            return True
        else:
            return False

    def loading_routes(self, fileName : str):
        file_path = os.path.join("./",fileName)
        with open(file_path, 'r') as json_file:
            self.routes_info = json.load(json_file)
            pass

    def add_nouce(self, nouce:str, route: str):
        self.nouce_map[nouce] = route
        print(self.nouce_map)
        return

    def boardcast_nouce(self, nouce: str, route: str):
        for other in self.known.copy():
            print(other)
            try:
                server = ServerProxy(other)
                server.add_nouce(nouce,route)
                # state
            except OSError:
                self.known.remove(other)
        return

    def add_others(self, ports: list):
        for p in ports:
            self.known.add("http://localhost:"+str(p)+"/")
        print(self.known)    

    def boardcast_boarding(self, ticket:str):
        return

    def check_remain(self, route_id:str):
        return(self.routes_info[route_id]["Remain"])

    def _start(self):
        s = SimpleXMLRPCServer(("localhost", self.port), allow_none = True)
        s.register_instance(self)
        s.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python3 server.py <port number> <route_file> <node_name>")
    port = int(sys.argv[1])
    route_file = sys.argv[2]
    name = sys.argv[3]
    ports.remove(port)
    node = Node(port, S1, S2, n, name,ports)
    node.loading_routes(route_file)
    node._start()
