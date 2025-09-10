import socket
import time
import math

# Server configuration
HOST = '192.168.0.91'  # IP address of the socket server
PORT = 1000            # Port number

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

        # Send the initial message
        message = 'START' + chr(13)  # Append carriage return
        s.sendall(message.encode('ascii'))
        print("Message sent:", repr(message))
        time.sleep(2)

        # Zig-zag scanning: alternate horizontal order per row.
        for i in range(nStepsY):
            if i % 2 == 0:
                # Even row: scan left-to-right.
                j_range = range(nStepsX)
            else:
                # Odd row: scan right-to-left.
                j_range = reversed(range(nStepsX))

            for j in j_range:
                # Calculate coordinates:
                #   y-coordinate based on row index, x-coordinate based on column index.
                x_coord = j * nStepX
                y_coord = i * nStepY
                print(f"Step: Row {i + 1}, Col {j + 1} -> Coordinates: ({x_coord:.1f}, {y_coord:.1f})")
                # Create the MOVE message; adjust field order if necessary.
                message = f'MOVE,{y_coord:.1f},{x_coord:.1f}' + chr(13)
                s.sendall(message.encode('ascii'))
                print("Message sent:", repr(message))
                time.sleep(1)
                data = s.recv(1024)
                print("Received:", data.decode())
                time.sleep(1)

        # Send the end message
        message = 'STOP' + chr(13)  # Append carriage return
        s.sendall(message.encode('ascii'))
        print("Message sent:", repr(message))
        time.sleep(2) 

except Exception as e:
    print("Socket error:", e)