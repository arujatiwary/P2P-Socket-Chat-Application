# P2P-Socket-Chat-Application
This project presents the design and implementation of a Peer-to-Peer (P2P) chat application using socket programming in Python. The application enables two users to establish a direct TCP connection and exchange messages in real-time without requiring a centralized server. The primary objectives were to gain hands-on experience with socket APIs, concurrency, and custom communication protocols.

The system was implemented using Python’s built-in socket and threading libraries, ensuring cross-platform compatibility and minimal external dependencies. The chat application supports usernames, graceful termination using the /quit command, and file transfer functionality through a simple custom protocol. The results demonstrate successful message exchange and attachment transfer between peers on the same network. This project highlights the importance of understanding fundamental networking concepts, concurrent programming, and protocol design in real-world applications.

# Files/Folders:
chat.py - Main python file.
Smaller Programs - Contains files of small programs that made up the main program. These were mainly used for understanding the working. A group server file is also included. It wasn't used in the main program though.
Report - A report on the implementation.
