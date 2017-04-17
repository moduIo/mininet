#-----------------------------------------------------------------------------
# Tim Zhang
# CSE534 HW3: Part C
# ---
# Program creates connections to each neighbor node and passes table data.
#-----------------------------------------------------------------------------
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
    message = socket.gethostname() + ' :'

    for route in routes:
        message += route + ';'

    s.send(message[:-1])
    s.close
