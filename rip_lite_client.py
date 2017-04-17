#
# Tim Zhang
# CSE534 HW3: Part C
# ---
# Program creates connections to each neighbor node and passes table data.
#
import socket
import sys

neighbors = sys.argv[1].split(',')  # CSV list of neighbor IP addresses

# Get routing table
with open('routing_tables/' + socket.gethostname() + '/routing_table.txt', 'r') as f:
    routes = f.read().splitlines()

# Send data to each neighbor
for neighbor in neighbors:
    # Create connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((neighbor, 800)) # IP address is passed in to client

    # Formatted table information
    s.send('CLIENT ROUTING TABLE\n' + socket.gethostname() + ' : ' + str(routes))

    #-------------------------------------    
    # MAYBE DELETE THIS
    #
    update = s.recv(1024)

    if update:
        print update
    #
    #
    #-------------------------------------
    s.close
