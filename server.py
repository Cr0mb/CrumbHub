import socket
import threading
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5555

# Function to derive encryption key from password
def derive_key(password):
    salt = b'salt_'  # Modify salt for production use
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to encrypt message
def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

# Function to decrypt message
def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    encrypted_data = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode()

# Server class handling connections
class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(5)
        self.clients = {}
        self.passwords = {}  # In production, use a secure method to store passwords

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                request = client_socket.recv(1024).decode()
                if request.startswith('REGISTER'):
                    _, username, password = request.split(' ')
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    self.passwords[username] = hashed_password
                    client_socket.send('Registration successful.'.encode())
                elif request.startswith('LOGIN'):
                    _, username, password = request.split(' ')
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if username in self.passwords and self.passwords[username] == hashed_password:
                        client_socket.send('Login successful.'.encode())
                        self.clients[username] = client_socket
                        self.handle_chat(username, client_socket)
                    else:
                        client_socket.send('Login failed.'.encode())
                elif request.startswith('MESSAGE'):
                    _, username, recipient, message = request.split(' ', 3)
                    if recipient in self.clients:
                        key = derive_key(self.passwords[recipient])
                        encrypted_message = encrypt_message(message, key)
                        self.clients[recipient].send(encrypted_message)
                    else:
                        client_socket.send(f'Error: {recipient} is not online.'.encode())
                elif request.startswith('LOGOUT'):
                    _, username = request.split()
                    del self.clients[username]
                    client_socket.send('Logout successful.'.encode())
                    break
                else:
                    client_socket.send('Error: Invalid command.'.encode())
            except Exception as e:
                print(f'Error handling client {client_address}: {str(e)}')
                break

    def handle_chat(self, username, client_socket):
        while True:
            try:
                request = client_socket.recv(1024)
                key = derive_key(self.passwords[username])
                decrypted_message = decrypt_message(request, key)
                print(f'{username}: {decrypted_message}')
            except Exception as e:
                print(f'Error handling chat for {username}: {str(e)}')
                break

    def start(self):
        print(f'Server listening on {SERVER_HOST}:{SERVER_PORT}...')
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'Accepted connection from {client_address}')
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

if __name__ == '__main__':
    server = ChatServer()
    server.start()
