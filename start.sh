python3 server.py 8001 routes.json node 1 &
python3 server.py 8002 routes.json node 2 &
python3 server.py 8003 routes.json node 3 &
python3 server.py 8004 routes.json node 4 &
python3 server.py 8005 routes.json node 5 &

sleep 3s

python3 client.py