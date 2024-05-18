import socket

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).


dst_ip = str(input("Enter Server IP: "))

s = socket.socket()
print ("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )
  recvmsg = c.recv(1024).decode()
  print('Server received '+recvmsg)
  c.send('Hello client'.encode())
  
  #Write your code here
  #1. Uncomment c.send 
  #2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response
  ##################

  c.close()
  #break