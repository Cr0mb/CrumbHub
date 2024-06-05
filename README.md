# CrumbHub
CrumbHub is a Python-based command-line chat application that facilitates real-time messaging and secure communication among multiple users over a network. It provides end-to-end encryption for messages using AES encryption and supports user registration, login, and basic chat functionalities.

# Features
```
> Secure Messaging: Messages are encrypted using AES encryption for secure transmission over the network.
> User Management: Supports user registration and login functionalities to manage user access.
> Real-Time Communication: Facilitates real-time messaging and chat sessions between connected users.
> Easy Setup: Simple setup and deployment for both server and client sides.
```

## Prerequisites

- Python 3.x installed on your system.

- cryptography library installed
  ``pip install cryptography``

## Server Setup

*** This python script needs also to be running on the server itself that this is hosted on

1. Clone the repository:
```
git clone https://github.com/Cr0mb/CrumbHub.git
cd CrumbHub
```

2. Modify the SERVER_HOST and SERVER_PORT constants in server.py to match your server configuration:
```
SERVER_HOST = 'your_server_ip_or_domain'
SERVER_PORT = 'server_port'
```
  
4. Start the server
```
python server.py
```

# How It Works

- Server Operation: The server manages incoming client connections, user registration/login, message encryption/decryption, and real-time chat sessions.

- Client Operation: Clients connect to the server using a Python script (client.py). They register/login securely and send encrypted messages to other connected users.


### Handling User Logins
```
1. Password Hashing
> When a user registers with the server, they provide a username and password.

> The password is immediately hashed using a cryptographic hash function (SHA-256 in this case) before being stored.

> This hashed password is what is actually saved in memory (in the passwords dictionary in the server script).

2. Storage Mechanism
> The hashed passwords (hashed_password) are stored in a dictionary (self.passwords) within the ChatServer class.

> This dictionary associates each username with its hashed password.

3. Login 
> When a user attempts to log in, the server retrieves the stored hashed password associated with the provided username.

> It then hashes the password attempt provided by the user and compares this hashed value with the stored hashed password.

> If the hashed values match, the login is successful; otherwise, it fails.
```
# INFO

- Do I need to keep the server running for others to connect?

> Yes the server must be running and accessible on a network-accessible server or machine for clients to connect to it and use the chat functionalities. Ensure your server environment allows inbound connections on the specified port (SERVER_PORT). If your having issues with this, make sure that the port is allowed through the firewall and that it is open.


- How do clients connect to the server?

> Clients connect to the server by specifying the server's IP address or domain name and the port number (SERVER_PORT) in the client script (client.py). Make sure these constants are set correctly also on the actual server, where the server_ip can be left as either the actual ip or just 0.0.0.0 .

- Is message transmission secure?

> Yes, the server uses AES encryption for message encryption and decryption. Messages are encrypted before transmission from the sender and decrypted upon receipt by the recipient, ensuring secure communication over the network.


