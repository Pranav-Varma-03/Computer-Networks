import socket

serverIP = "10.0.1.2"

dst_ip = str(input("Enter dstIP: "))
s = socket.socket()

print(dst_ip)

port = 12346

s.connect((dst_ip, port))

#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.
#2. Add the code to parse the response you get from the server.
s.send('Hello server'.encode())
print ('Client received '+s.recv(1024).decode())

s.close()
