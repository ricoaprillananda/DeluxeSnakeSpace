import pygame
import socket
import threading
import pickle 

# Basic configuration for the network
HOST = "localhost"  
PORT = 5555 
BUFFER_SIZE = 4096  

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))  
        self.username = None

    def send(self, data):
        """Send data to the server"""
        try:
            message = pickle.dumps(data)  
            self.client.send(message)
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive(self):
        """Receive data from the server"""
        try:
            message = self.client.recv(BUFFER_SIZE) 
            return pickle.loads(message) 
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def close(self):
        """Close the connection"""
        self.client.close()

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))  
        self.server.listen(5)  
        self.clients = []  
        self.nicknames = []  

        print("Server started...")
        self.accept_clients()  

    def broadcast(self, message):
        """Broadcast the message to all clients"""
        for client in self.clients:
            try:
                client.send(message) 
            except Exception as e:
                print(f"Error broadcasting message: {e}")

    def handle_client(self, client):
        """Handle individual client communication"""
        try:
            while True:
                message = client.recv(BUFFER_SIZE) 
                if message:
                    self.broadcast(message)  
                else:
                    break
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.clients.remove(client)  
            client.close() 

    def accept_clients(self):
        """Accept incoming client connections"""
        while True:
            client, address = self.server.accept()
            print(f"New connection: {address}")
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start() 

# Game Client class
class GameClient:
    def __init__(self):
        self.network = Network() 
        self.running = True

    def run(self):
        """Run the game client, handle sending and receiving messages"""
        while self.running:
            # For now, the client can send a simple message or game state
            message = input("Enter message to send to the server: ")
            if message.lower() == "quit":
                self.running = False
                break
            self.network.send(message)  
            response = self.network.receive()  
            if response:
                print(f"Server response: {response}")
        self.network.close()  

# Game Server class
class GameServer:
    def __init__(self):
        self.server = Server()

    def start(self):
        """Start the game server to handle multiple clients"""
        pass  

if __name__ == "__main__":
    mode = input("Enter 'server' to start server or 'client' to start client: ").strip().lower()

    if mode == "server":
        server = GameServer() 
    elif mode == "client":
        client = GameClient()  
        client.run()  