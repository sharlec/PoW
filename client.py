import xmlrpc.client
import hashlib
import time

def compute(key: str, n: int):
    i = 0
    while True:
        key2 = key + str(i)
        key3 = key2.encode('ascii')
        outcome = hashlib.sha256(key3).hexdigest()
        checker = "0" * n
        if outcome[:n] == checker:
            return key2
        i = i + 1

class Box:
	def __init__(self,tk):
		self.routes = ( "K98665", 
                        "K67332",
	                    "D66775")
		self.box = ttk.Combobox(tk, values = self.routes)
		self.box.place(x = 150, y=200)
		self.button = Button(tk, text = "Buy", command=self.select).place(x = 200, y = 300)

	def select(self):
		value = self.box.get()
		print(value)
		ticket = buy_ticket(value)
		if ticket != False:
			messagebox.showinfo("showinfo", ticket)

def buy_ticket(route: str):
	t1 = time.time()
	with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
		key,n = proxy.get_nouce(route)
	key2 = compute(key,n)

	with xmlrpc.client.ServerProxy("http://localhost:8002/") as proxy:
		outcome = proxy.get_ticket(key2)
		print(outcome)
	t2 = time.time()
	print(t2 - t1)
	return outcome

if __name__ == "__main__":
	buy_ticket("K98665")
