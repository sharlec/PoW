# %%
import xmlrpc.client
import hashlib
import time
# %%

def buy_ticket(route: str):
	t1 = time.time()

	with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
	    key,n = proxy.get_nouce(route)
	# %%
	key2 = compute(key,n)


	with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
	    outcome = proxy.get_ticket(key2)
	    print(outcome)
	t2 = time.time()
	print(t2 - t1)
	return outcome

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

def main():
	buy_ticket("K98665")

if __name__ == "__main__":
	main()