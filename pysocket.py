import socket

resp = {}

def handle_client(client_socket):
	while(True):
		request = (client_socket.recv(1024).decode('utf-8')).split()  # Receive data from the client (up to 1024 bytes)
		print(request)
		if not request:
			break
		if request[0] == "get":
			if len(request) == 2 and request[1] in resp:
				response = resp[request[1]]+"\n"
			else:
				response = "Key value pair does not exist\n"
			client_socket.send(response.encode('utf-8'))  # Send a response back to the client
		elif request[0] == "set":
			if len(request) == 3:
				resp[request[1]] = request[2]
			else:
				response = "Enter a value for the key\n"
				client_socket.send(response.encode('utf-8'))  # Send a response back to the client
		elif request[0] == "del":
			if len(request) == 2 and request[1] in resp:
				resp.pop(request[1])
			else:
				response = "Key value pair does not exist\n"
		elif request[0] == "dc":
			break
		else:
			response = "Invalid Command\n"
			client_socket.send(response.encode('utf-8'))  # Send a response back to the client
	client_socket.close()  # Close the client socket

def main():
	server_host = '127.0.0.1'  # Listen on localhost (change to 0.0.0.0 to accept connections from any IP)
	server_port = 14001       # Choose an available port (e.g., above 1024)

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
	server_socket.bind((server_host, server_port))  # Bind the socket to a host and port
	server_socket.listen(1)  # Start listening for incoming connections (up to 1 connection)

	print(f"Server listening on {server_host}:{server_port}")

	while True:
		client_socket, client_address = server_socket.accept()  # Accept incoming connections
		print(f"Accepted connection from: {client_address[0]}:{client_address[1]}")
		handle_client(client_socket)  # Handle the client's request
	server_socket.close()

if __name__ == "__main__":
	main()
