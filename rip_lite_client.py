#
# Tim Zhang
# CSE534 HW3: Part C
#
import socket
import sys

neighbors = sys.argv[1].split(',')  # CSV list of neighbor IP addresses


for neighbor in neighbors:
    # Create connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((neighbor, 800)) # IP address is passed in to client

    with open('routing_tables/' + socket.gethostname() + '/routing_table.txt', 'r') as f:
        routes = f.read().splitlines()

    s.send('CLIENT ROUTING TABLE\n' + ' node-' + socket.gethostname() + ' : ' + str(routes))
    
    update = s.recv(1024)

    if update:
        print update
    
    s.close
