#-----------------------------------------------------------------------------
# Tim Zhang
# CSE534 HW3: Part C
# ---
# Program runs "server" processes on each of the nodes which waits for 
# each neighbor to pass in routing table information.
# Once this data is received the server will update routing info and
# pass to neighbors.
#-----------------------------------------------------------------------------
import socket
import sys
import os
import re
import time
from datetime import datetime

#
# Implements Bellman-Ford algorithm
#
def compute_tables(tables, routes, neighbors):
    dests = {}          # (key, value) pairs (dest, {next, cost})
    updatedRoutes = {}  # Holds updated routing table
    costs = {}          # Holds current cost to node
    host = socket.gethostname()

    # Set up host entry
    dests[host] = host + ',0'
    costs[host] = 0

    # Split routes into dictionary keyed by dest
    for route in routes:
        data = route.split(',')
	dests[data[0]] = data[1] + ',' + data[2]
        costs[data[0]] = int(data[2])

    # For all neighbor distance vectors
    for neighbor in neighbors:
        entries = tables[neighbor].split(';')
	
        # For each table entry
	for entry in entries:
	    field = entry.split(',')
	    cost = costs[neighbor] + int(field[2])

            # If the dest was not already in the DV simply add it
            if not field[0] in dests:
                dests[field[0]] = neighbor + ',' + str(cost)
                costs[field[0]] = cost

            # Otherwise add if new path is shorter, but don't go negative
            elif cost < costs[field[0]] and cost > 0:
                dests[field[0]] = neighbor + ',' + str(cost)
                costs[field[0]] = cost

    # Fill in new DV
    for dest in dests.keys():
        updatedRoutes[dest] = dests[dest]

    return 'TABLES: ' + str(tables) + '\nROUTES' + str(routes) + '\nUPDATED ROUTES: ' + str(updatedRoutes) + '\n'

#
# Main()
#
iteration = 1      # Tracks iteration for message synchronization
neighbors = []     # Holds neighbor names prepended
neighbor_ips = []  # Holds IP addresses of neighbors
tables = {}        # Holds tables of neighbors

# Create neighbor arrays from command line
for neighbor in sys.argv[1].split(','):
    neighbors.append(neighbor)

for ip in sys.argv[2].split(','):
    neighbor_ips.append(ip)

# Setup server socket on port 800
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 800))
host = socket.gethostname()

# Enforce fresh routing_table.txt
table_path = 'routing_tables/' + host + '/routing_table.txt'
open(table_path, 'w').close()
table = open(table_path, 'w')

# Parse weights.txt file to get initial routing tables
with open('weights.txt', 'r') as f:
    for weight in f:
	entry = weight.split(',')

        # Store edge weights of incident links
        if host in entry:
            cost = entry[2].strip()

	    if host == entry[0]:
	        dest = entry[1]
	    else:
		dest = entry[0]

            # Create application layer routing table file in CSV format
            # Format: dest, cost, next
            table.write(dest + ',' + dest + ',' + cost + '\n')

table.close()

# Get routing information stored in CSV
with open(table_path, 'r') as f:
    routes = f.read().splitlines()

serverSocket.listen(5)

# Main computation loop
while True:
    (clientSocket, address) = serverSocket.accept()
    message = clientSocket.recv(1024)    
    
    # Check which neighbor sent the message
    for neighbor in neighbors:
        if neighbor in message:
            # Add routing table to dict
	    tables[neighbor] = message.split(':', 1)[-1]

    # If all of the neighbors have passed data
    if len(tables) == len(neighbors):
        done = open('done.txt', 'a+')  # Text file of tally marks
	done.write('x')
        done.close()

	# Halt until all other servers are complete
        done = open('done.txt', 'r')
        completed = len(done.read())  # Number of hosts which are done
        done.close()

        while completed < iteration * 6:
            clientSocket.close()
	    time.sleep(.1)
            done = open('done.txt', 'r')
            completed = len(done.read())
            done.close()

	# Compute new tables
	foo = open('foo.txt', 'a+')
	foo.write(host + ' : ' + str(compute_tables(tables, routes, neighbors)) + '\n')
	foo.close()

	# Write completion time to log.txt
	log = open('log.txt', 'a+')
	log.write(host + ' completed iteration ' + str(iteration) + ' at ' + str(datetime.now()) + '\n')
	log.close()
	
        iteration += 1 # Track iteration for synchronization
    
    clientSocket.close()
