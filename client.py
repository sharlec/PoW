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