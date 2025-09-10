import socket
import time

# Server configuration
HOST = '192.168.0.91'  # IP address of the socket server
PORT = 1000            # Port number

# Message to send
message = 'START' + chr(13)  # Append ASCII 13 (carriage return)

try:
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to server
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # Send the message
        s.sendall(message.encode('ascii'))
        print("Message sent:", repr(message))
        time.sleep(2)

        # Optional: receive response (uncomment if needed)
        # data = s.recv(1024)
        # print("Received:", data.decode())

        for i in range(100):
            print("Iteration:", i + 1)
            # Optional: sleep or perform other operations here
            message = 'MOVE' + chr(13) 
            s.sendall(message.encode('ascii'))
            print("Message sent:", repr(message))
            time.sleep(1)
            data = s.recv(1024)
            print("Received:", data.decode())
            time.sleep(1)


except Exception as e:
    print("Socket error:", e)