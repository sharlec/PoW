# %%
import string   
import random 
import hashlib    
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys
import json
import os

# %%
S1 = 10 # num of digits of the random keywords
S2 = 16 # num of digits of the tickets
n = 5
ports = [8000,8001,8002,8003]
# %%
class Node:
    def __init__(self, port, S1, S2, n):
        self.port = port
        self.nouce_length = S1
        self.ticket_length = S2
        self.n = n
        self.routes_info = {}
        self.nouce_map = {}
        self.ticket_map = {}

    def randomString(self, k):  
        ranKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k = k)) 
        return ranKey

    def get_nouce(self, route:str):
        if route in self.routes_info.keys():
            nouce = self.randomString(S1)
            self.nouce_map[nouce] = route
            return nouce, n
        else:
            return False

    def get_ticket(self, key: str):
        if key[:S1] not in self.nouce_map.keys():
            return False
        key2 = key.encode('ascii')
        outcome = hashlib.sha256(key2).hexdigest()
        checker = "0" * n
        if outcome[:n] == checker:
            ticket = self.randomString(S2)
            self.ticket_map[ticket] = {"valid": True}
            return ticket
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

    def boardcast_nouce(self, nouce: str, route_id: str):
        return


    def boardcast_ticket(self, ticket:str, route_id: str):
        return

    def boardcast_boarding(self, ticket:str):
        return

    def _start(self):
        s = SimpleXMLRPCServer(("localhost", self.port))
        s.register_instance(self)
        s.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python3 server.py <port number> <route_file>")
    port = int(sys.argv[1])
    route_file = sys.argv[2]

    node = Node(port, S1, S2, n)
    node.loading_routes(route_file)
    node._start()

