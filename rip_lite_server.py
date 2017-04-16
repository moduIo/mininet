#
# Tim Zhang
# CSE534 HW3: Part C
#
import socket
import sys

# Setup server socket on port 800
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 800))
host = socket.gethostname()

# Enforce freash routing_table.txt
table_path = 'routing_tables/' + host + '/routing_table.txt'
open(table_path, 'w').close()
table = open(table_path, 'w')

# Parse weights.txt file to get relevant weights
with open('weights.txt', 'r') as f:
    for weight in f:

        # Store edge weights of incident links
        if host in weight:
            
            # Create application layer routing table file in CSV format
            table.write(weight)

table.close()

# Get routing information stored in CSV on single line
with open(table_path, 'r') as f:
    routes = f.read().splitlines()

serverSocket.listen(5)

# Main computation loop
while True:
    (clientSocket, address) = serverSocket.accept()
    message = clientSocket.recv(1024)    
    clientSocket.send(message + '\n')
    clientSocket.send('SERVER SAYS ' + host + ' routing table: ' + str(routes))
    clientSocket.close()
