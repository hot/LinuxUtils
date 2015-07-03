import socket

bind_ip = "0.0.0.0"
bing_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client.connect((bind_ip, bing_port))

f = open("README.md", 'rb')

print "start sending..."

data = f.read(1024)

while data:
    print 'sending..'
    client.send(data)
    data = f.read(1024)

f.close()
print 'Done sending'

#tell server sending is over
client.shutdown(socket.SHUT_WR)

print client.recv(1024)

client.close()
