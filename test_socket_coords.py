import socket
import time

# Server configuration
HOST = '192.168.0.91'  # IP address of the socket server
PORT = 1000            # Port number


import math

# Parámetros de escaneo
nWidthX = 150
nWidthY = 200
nOffsX = 25
nOffsY = 25
nOverlap = 50  # Porcentaje

# Cálculo de pasos efectivos
nStepX = nOffsX * (1 - nOverlap / 100)
nStepY = nOffsY * (1 - nOverlap / 100)

# Cálculo del número de pasos (equivalente a roundDown en VAL3)
nStepsX = math.floor((nWidthX - nOffsX) / nStepX) + 1
nStepsY = math.floor((nWidthY - nOffsY) / nStepY) + 1

# Mostrar resumen
print("Scan Data:")
print("   Scan Area:")
print(f"      X: {nWidthX:.1f} mm")
print(f"      Y: {nWidthY:.1f} mm")
print("   Offset and Overlap:")
print(f"      OffsX: {nOffsX:.1f} mm")
print(f"      OffsY: {nOffsY:.1f} mm")
print(f"      Overlap: {nOverlap:.1f} %")
print("   Steps:")
print(f"      nStepsX: {nStepsX}")
print(f"      nStepsY: {nStepsY}")
print()


try:
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to server
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # Send the message
        message = 'START' + chr(13)  # Append ASCII 13 (carriage return)
        s.sendall(message.encode('ascii'))
        print("Message sent:", repr(message))
        time.sleep(2)

        # Optional: receive response (uncomment if needed)
        # data = s.recv(1024)
        # print("Received:", data.decode())

        for i in range(nStepsY):
            for j in range(nStepsX):
                print(f"Step: ({i + 1}, {j + 1})")
                # Optional: sleep or perform other operations here
                message = f'MOVE,{i * nStepY:.1f},{j * nStepX:.1f}' + chr(13)
                #message = 'MOVE' + chr(13)  # Append ASCII 13 (carriage return)
                s.sendall(message.encode('ascii'))
                print("Message sent:", repr(message))
                time.sleep(1)
                data = s.recv(1024)
                print("Received:", data.decode())
                time.sleep(1)


except Exception as e:
    print("Socket error:", e)