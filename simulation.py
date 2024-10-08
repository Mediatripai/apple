# Import necessary libraries
import argparse
from queue import Queue

# Define a class to represent a request
class Request:
    def __init__(self, timestamp, processing_time):
        # Initialize request attributes
        self.timestamp = timestamp
        self.processing_time = processing_time

    # Method to get the request's timestamp
    def get_timestamp(self):
        return self.timestamp

    # Method to get the request's processing time
    def get_processing_time(self):
        return self.processing_time


# Define a class to represent a server
class Server:
    def __init__(self):
        # Initialize server attributes
        self.current_request = None  # current request being processed
        self.time_remaining = 0  # remaining processing time

    # Method to simulate one tick of the server's clock
    def tick(self):
        if self.current_request:
            # Decrement the remaining processing time
            self.time_remaining -= 1
            # If there is no more processing time, mark the request as completed
            if self.time_remaining <= 0:
                self.current_request = None

    # Method to check if the server is busy
    def busy(self):
        return self.current_request is not None

    # Method to start a new request on the server
    def start_next(self, new_request):
        # Set the current request to the new request
        self.current_request = new_request
        # Set the remaining processing time to the length of the new request's processing time
        self.time_remaining = new_request.get_processing_time()


# Function to simulate one server with a given file
def simulateOneServer(filename):
    # Create a new server object
    server = Server()
    # Create a queue to hold requests
    request_queue = Queue()
    # List to store wait times for each request
    wait_times = []

    # Open the input file and read it line by line
    with open(filename, 'r') as f:
        for line in f:
            # Split the line into timestamp, processing time, and other data
            data = line.split(',')
            timestamp = int(data[0])  # Get the request's timestamp
            processing_time = int(data[2])  # Get the request's processing time
            # Create a new request object and add it to the queue
            request = Request(timestamp, processing_time)
            request_queue.put(request)

    # Initialize the current second to 0
    current_second = 0
    while not request_queue.empty():
        # If there are no requests in the queue or the server is busy, wait for a new request
        if not server.busy() and not request_queue.empty():
            next_request = request_queue.get()
            # Start the new request on the server
            server.start_next(next_request)
            # Calculate the wait time for the request
            wait_time = current_second - next_request.get_timestamp()
            # Add the wait time to the list of wait times
            wait_times.append(wait_time)

        # Simulate one tick of the server's clock
        server.tick()
        # Increment the current second
        current_second += 1

    # Calculate and return the average wait time for all requests
    average_wait = sum(wait_times) / len(wait_times)
    return average_wait


# Function to simulate multiple servers with a given file
def simulateManyServers(filename, num_servers):
    # Create a list of server objects
    servers = [Server() for _ in range(num_servers)]
    # Create a queue to hold requests
    request_queue = Queue()
    # List to store wait times for each request
    wait_times = []

    # Open the input file and read it line by line
    with open(filename, 'r') as f:
        for line in f:
            # Split the line into timestamp, processing time, and other data
            data = line.split(',')
            timestamp = int(data[0])  # Get the request's timestamp
            processing_time = int(data[2])  # Get the request's processing time
            # Create a new request object and add it to the queue
            request = Request(timestamp, processing_time)
            request_queue.put(request)

    # Initialize the current second to 0
    current_second = 0
    server_index = 0
    while not request_queue.empty():
        # Get the next available server and start a new request on it if necessary
        server = servers[server_index]
        if not server.busy() and not request_queue.empty():
            next_request = request_queue.get()
            # Start the new request on the server
            server.start_next(next_request)
            # Calculate the wait time for the request
            wait_time = current_second - next_request.get_timestamp()
            # Add the wait time to the list of wait times
            wait_times.append(wait_time)

        # Simulate one tick of each server's clock
        for s in servers:
            s.tick()

        # Increment the current second and move to the next server
        current_second += 1
        server_index = (server_index + 1) % num_servers

    # Calculate and return the average wait time for all requests
    average_wait = sum(wait_times) / len(wait_times)
    return average_wait


# Main function
def main():
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help="CSV file with requests")
    parser.add_argument('--servers', type=int, help="Number of servers to simulate")
    args = parser.parse_args()

    if args.servers:
        # Simulate multiple servers and print the result
        avg_wait = simulateManyServers(args.file, args.servers)
        print(f"Average wait time for {args.servers} servers: {avg_wait:.2f} seconds")
    else:
        # Simulate one server and print the result
        avg_wait = simulateOneServer(args.file)
        print(f"Average wait time for one server: {avg_wait:.2f} seconds")


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

"""
Running the Simulation
For one server:
Copy code
python simulation.py --file test.csv

For multiple servers (e.g., 3 servers):
Copy code
python simulation.py --file test.csv --servers 3
This will simulate the requests in test.csv with either a single server or multiple servers, 
depending on the provided command-line arguments.
"""